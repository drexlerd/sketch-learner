/*
Lightweight Automated Planning Toolkit
Copyright (C) 2012
Miquel Ramirez <miquel.ramirez@rmit.edu.au>
Nir Lipovetzky <nirlipo@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef __SKETCH_SIW__
#define __SKETCH_SIW__

#include <aptk/search_prob.hxx>
#include <aptk/resources_control.hxx>
#include <aptk/closed_list.hxx>
#include <aptk/iw.hxx>
#include <landmark_graph.hxx>
#include <vector>
#include <algorithm>
#include <iostream>
#include <action.hxx>

#include <dlplan/policy.h>


namespace aptk {

namespace search {


template < typename Search_Model >
class Sketch_SIW : public brfs::IW<Search_Model, aptk::agnostic::Novelty<Search_Model, aptk::search::brfs::Node< aptk::State >>> {

public:

	typedef		aptk::search::brfs::Node< aptk::State >		Search_Node;
	typedef		aptk::agnostic::Landmarks_Graph				Landmarks_Graph;
	typedef		typename Search_Model::State_Type		                          State;
	typedef 	Closed_List< Search_Node >			                          Closed_List_Type;

	Sketch_SIW( const Search_Model& search_problem )
		: brfs::IW<Search_Model, aptk::agnostic::Novelty<Search_Model, Search_Node>>( search_problem ),
		  m_pruned_sum_B_count(0), m_sum_B_count(0), m_max_B_count(0), m_iw_calls(0), m_max_bound( std::numeric_limits<unsigned>::max() ), m_closed_goal_states( NULL ),
		  m_dlplan_initial_state(static_cast<const Sketch_STRIPS_Problem*>(&search_problem.task())->get_default_state()) {
		m_goal_agenda = NULL;
		m_sketch_problem = static_cast<const Sketch_STRIPS_Problem*>(&search_problem.task());
	}

	virtual ~Sketch_SIW() {
	}
	void            set_goal_agenda( Landmarks_Graph* lg ) { m_goal_agenda = lg; }

    /**
	 * Calls IW for each subproblem encountered
	 */
	virtual bool	find_solution( float& cost, std::vector<Action_Idx>& plan, std::vector<std::vector<Action_Idx>>& partial_plans, std::vector<std::string>& sketch_plan, std::vector<unsigned>& subproblem_widths) {

		unsigned gsize = this->problem().task().goal().size();
		Search_Node* end = NULL;
		State* new_init_state = NULL;

		cost = 0;

		new_init_state = new State( this->problem().task() );
		new_init_state->set( this->m_root->state()->fluent_vec() );
		this->start( new_init_state );
        // new_init_state->print( std::cout );

        m_sketch = m_sketch_problem->sketch();

		// count the number of sketch rules applied s.t. we can terminate in the case of a cycle
		int count_applied_sketch_rules = 0;
		const int max_applied_sketch_rules = 100000;

		do{
			if ( this->verbose() )
				//std::cout << std::endl << "{" << gsize << "/" << this->m_goal_candidates.size() << "/" << this->m_goals_achieved.size() << "}:IW(" << this->bound() << ") -> ";

            // We must reset cache because indices start from 0 again.
		    m_denotation_caches = dlplan::core::DenotationsCaches();
            m_dlplan_initial_state = m_sketch_problem->from_lapkt_state(new_init_state, new_init_state->index());
			// new_init_state->print( std::cout );
		    m_rules = m_sketch->evaluate_conditions_eager(m_dlplan_initial_state, m_denotation_caches);
			end = this->do_search();
			m_pruned_sum_B_count += this->pruned_by_bound();

			if ( end == NULL ) {
				/**
				 * If no partial plan to achieve any goal is  found,
				 * throw IW(b+1) from same root node
				 *
				 * If no state has been pruned by bound, then IW is in a dead-end,
				 * return NO-PLAN
				 */
				if( this->pruned_by_bound() == 0)
					return false;

				new_init_state = new State( this->problem().task() );
				new_init_state->set( this->m_root->state()->fluent_vec() );
				new_init_state->update_hash();

				if ( this->bound() > this->max_bound() ) // Hard cap on width exceeded
					return false;

				this->set_bound( this->bound()+1 );
				this->start( new_init_state );

				// Memory exceeded to reserve data structures for novelty
				if(this->m_novelty->arity() != this->bound() )
					return false;
			}
			else{

				/**
				 * If a partial plan extending the achieved goals set is found,
				 * IW(1) is thrown from end_state
				 */

				std::vector<Action_Idx> partial_plan;
				float partial_cost = 0.0f;
				this->extract_plan( this->m_root, end, partial_plan, partial_cost );
				std::cout << "\n";

				std::vector<Search_Node*> partial_path;
				this->extract_path( this->m_root, end, partial_path );
				plan.insert( plan.end(), partial_plan.begin(), partial_plan.end() );
				partial_plans.push_back(partial_plan);
				sketch_plan.push_back(m_key_applied_rule);
				std::cout << "applied rule: " << m_key_applied_rule << " ";

                // we use <= instead of = to ensure that width is observed as 0 if the empty plan solves the instance.
                int width = (partial_plan.size() <= 1) ? 0 : this->bound();
				subproblem_widths.push_back(width);
				m_max_B_count = m_max_B_count < this->bound() ? width : m_max_B_count;
				m_sum_B_count += width;
				m_iw_calls++;

				cost += partial_cost;
				++count_applied_sketch_rules;
				if (count_applied_sketch_rules == max_applied_sketch_rules) {
					std::cout << std::endl << "Reached maxmimum of allowed sketch rules: " << max_applied_sketch_rules << std::endl;
					return false;
				}

				std::cout << "\n";

				new_init_state = new State( this->problem().task() );
				new_init_state->set( end->state()->fluent_vec() );
				new_init_state->update_hash();

				this->set_bound( 1 );
				this->start( new_init_state );
			}
		} while( !this->problem().goal( *new_init_state ) );

		return true;
	}

	/**
	 * Starts a new IW search if new subproblem is encountered.
	 */
	virtual bool  is_goal( Search_Node* n ) {
		State* s = n->state();
		assert(s != NULL);

		dlplan::core::State dlplan_target_state = m_sketch_problem->from_lapkt_state(s, s->index());
		const auto evaluation_result = m_sketch->evaluate_effects_lazy(m_dlplan_initial_state, dlplan_target_state, m_rules, m_denotation_caches);
		if (evaluation_result) {
			m_key_applied_rule = evaluation_result->compute_repr();
			return true;
		}
		/* 2. Check whether s is an overall goal of the problem. */
		if (this->problem().goal(*s)) {
		    return true;
		}
		return false;
	}

	unsigned		sum_pruned_by_bound() const		{ return m_pruned_sum_B_count; }
	float                   avg_B() const { return (float)(m_sum_B_count) / m_iw_calls; }
	unsigned                max_B() const { return m_max_B_count; }
	void			set_max_bound( unsigned v ) { m_max_bound = v; }
	unsigned		max_bound( ) { return m_max_bound; }

protected:
	unsigned		m_pruned_sum_B_count;
	unsigned		m_sum_B_count;
	unsigned		m_max_B_count;
	unsigned		m_iw_calls;
	Landmarks_Graph*        m_goal_agenda;
	unsigned		m_max_bound;

	Closed_List_Type*			m_closed_goal_states;

	// sketch related information
	const Sketch_STRIPS_Problem* m_sketch_problem;
	std::shared_ptr<const dlplan::policy::Policy> m_sketch;
	dlplan::core::DenotationsCaches m_denotation_caches;

	dlplan::core::State m_dlplan_initial_state;
	std::vector<std::shared_ptr<const dlplan::policy::Rule>> m_rules;

	std::string m_key_applied_rule;
};

}

}



#endif // Sketch_siw.hxx
