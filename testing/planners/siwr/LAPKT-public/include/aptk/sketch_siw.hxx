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
#include <dlplan/evaluator.h>


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
		  m_pruned_sum_B_count(0), m_sum_B_count(0), m_max_B_count( 0 ), m_iw_calls(0), m_max_bound( std::numeric_limits<unsigned>::max() ), m_closed_goal_states( NULL ),
		  m_sketch_problem(static_cast<const Sketch_STRIPS_Problem*>(&search_problem.task())),
		  m_sketch(static_cast<const Sketch_STRIPS_Problem*>(&search_problem.task())->sketch()),
		  m_evaluation_cache(dlplan::evaluator::EvaluationCache(0, 0)) {
	}

	virtual ~Sketch_SIW() {
	}

    /**
	 * Calls IW for each subproblem encountered
	 */
	virtual bool	find_solution( float& cost, std::vector<Action_Idx>& plan, std::vector<std::vector<Action_Idx>>& partial_plans, std::vector<std::string>& sketch_plan, std::vector<unsigned>& subproblem_widths) {
		Search_Node* end = NULL;
		State* new_init_state = NULL;

		cost = 0;

        //std::cout << this->m_gen_count << std::endl;
		//abort();
		if (this->generated() != 1) {
			throw std::runtime_error("The initial state should have been generated.");
		}
		new_init_state = new State( this->problem().task(), 0 );
		new_init_state->set( this->m_root->state()->fluent_vec() );

		m_evaluation_cache = dlplan::evaluator::EvaluationCache(m_sketch.get_boolean_features().size(), m_sketch.get_numerical_features().size());
        dlplan::core::State dlplan_initial_state = m_sketch_problem->from_lapkt_state(new_init_state);
		m_initial_state_context = new dlplan::evaluator::EvaluationContext(dlplan_initial_state, m_evaluation_cache);

		m_rules = m_sketch.evaluate_conditions_eager(*m_initial_state_context);
		m_lapkt_initial_state = new_init_state;

		// count the number of sketch rules applied s.t. we can terminate in the case of a cycle
		int count_applied_sketch_rules = 0;
		const int max_applied_sketch_rules = 10000;
		do {
			if (this->bound() == 0) {
				// check 1-step successors.
				end = this->do_search_iw_0();
			} else if (this->bound() > 0) {
				// run usual IW(k) searches with k=1,2.
				end = this->do_search();
			}
			//end = this->do_search();
			m_pruned_sum_B_count += this->pruned_by_bound();

			if ( end == NULL ) {
				/**
				 * If no partial plan to achieve any goal is  found,
				 * throw IW(b+1) from same root node
				 *
				 * If no state has been pruned by bound, then IW is in a dead-end,
				 * return NO-PLAN
				 */
				if( this->bound() > 0 && this->pruned_by_bound() == 0) {
					return false;
				}

				new_init_state = new State( this->problem().task(), m_lapkt_initial_state->index());
				new_init_state->set( this->m_root->state()->fluent_vec() );
				new_init_state->update_hash();
				m_lapkt_initial_state = new_init_state;

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
                /*for ( unsigned k = 0; k < partial_plan.size(); k++ ) {
					std::cout << k+1 << ". ";
					const aptk::Action& a = *(m_sketch_problem->actions()[ partial_plan[k] ]);
					std::cout << a.signature();
					std::cout << std::endl;
				}*/
				std::cout << "\n";


				std::vector<Search_Node*> partial_path;
				this->extract_path( this->m_root, end, partial_path );
				//std::cout << std::endl;
				// std::cout << m_dlplan_initial_state->str() << std::endl;
				//std::unique_ptr<dlplan::core::State> dlplan_target_state;
				// std::cout << partial_plan.size() << std::endl;
				//for ( unsigned k = 0; k < partial_plan.size(); k++ ) {
				//	std::cout << k+1 << ". ";
				//	//partial_path[k]->state()->print(std::cout);
				//	dlplan_target_state = std::unique_ptr<dlplan::core::State>(new dlplan::core::State(m_sketch_problem->from_lapkt_state(partial_path[k]->state())));
		        //    const aptk::Action* a = this->problem().task().actions()[ partial_plan[k] ];
				//	//std::cout << a->signature() << " " << target_state_valuation.str() << std::endl;
				//}
				// if (dlplan_target_state) std::cout << dlplan_target_state->str() << std::endl << std::endl;

				plan.insert( plan.end(), partial_plan.begin(), partial_plan.end() );
				partial_plans.push_back(partial_plan);
				sketch_plan.push_back(m_key_applied_rule);
				std::cout << "applied rule: " << m_key_applied_rule << " ";

                // we use <= instead of = to ensure that width is observed as 0 if the empty plan solves the instance.
				subproblem_widths.push_back(this->bound());
				m_max_B_count = std::max<int>(this->bound(), m_max_B_count);
				m_sum_B_count += this->bound();
				m_iw_calls++;

				cost += partial_cost;
				++count_applied_sketch_rules;
				if (count_applied_sketch_rules == max_applied_sketch_rules) {
					std::cout << std::endl << "Reached maxmimum of allowed sketch rules: " << max_applied_sketch_rules << std::endl;
					return false;
				}

				std::cout << "\n";

				new_init_state = new State( this->problem().task(), end->state()->index() );
				new_init_state->set( end->state()->fluent_vec() );
				new_init_state->update_hash();
				m_lapkt_initial_state = new_init_state;

				this->set_bound( 0 );
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
        /* if goal state is closed then don't waste time with expensive computation. */
		if( is_goal_state_closed( n ) ) {
			return false;
		}
		//std::cout << "goal check" << std::endl;
		dlplan::core::State dlplan_target_state = m_sketch_problem->from_lapkt_state(s);
		dlplan::evaluator::EvaluationContext* target_state_context = new dlplan::evaluator::EvaluationContext(dlplan_target_state, m_evaluation_cache);
		//std::cout << m_lapkt_initial_state->index() << " " << s->index() << std::endl;
		const auto satisfied_rule = m_sketch.evaluate_effects_lazy(*m_initial_state_context, *target_state_context, m_rules);
		if (satisfied_rule) {
			// detect cycle in same state, i.e., no progress
			//if (this->root() != n) {
				m_key_applied_rule = satisfied_rule->compute_repr();
				delete m_initial_state_context;
				m_initial_state_context = target_state_context;
				m_lapkt_initial_state = s;
				// after refreshing the caches we can start with evaluation.
				m_rules = m_sketch.evaluate_conditions_eager(*m_initial_state_context);
				close_goal_state( n );
				return true;
			//}
		}
		/* 2. Check whether s is an overall goal of the problem. */
		if (this->problem().goal(*s)) {
			delete m_initial_state_context;
		    close_goal_state( n );
		    return true;
		}
		return false;
	}


	void set_closed_goal_states( Closed_List_Type* c ){ m_closed_goal_states = c; }
	void close_goal_state( Search_Node* n ) 	 {
		if( closed_goal_states() ){
			//m_closed_goal_states->put( n );
			State* new_state = new State( this->problem().task(), this->m_gen_count );
			new_state->set( n->state()->fluent_vec() );
			new_state->update_hash();
			Search_Node* new_node = new Search_Node( new_state, n->action() );
			new_node->gn() = n->gn();
			m_closed_goal_states->put( new_node );
		}
	}
	Closed_List_Type* closed_goal_states() { return m_closed_goal_states; }


	void reset_closed_goal_states( ) {
		if( closed_goal_states() ){
			// for ( typename Closed_List_Type::iterator i = m_closed_goal_states->begin();
			//       i != m_closed_goal_states->end(); i++ ) {
			// 	i->second = NULL;
			// }
			m_closed_goal_states->clear();
		}
	}


	bool is_goal_state_closed( Search_Node* n ) {
		if( !closed_goal_states() ) return false;

		n->compare_only_state( true );
		Search_Node* n2 = this->closed_goal_states()->retrieve(n);
		n->compare_only_state( false );

		if ( n2 != NULL )
			return true;

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
	unsigned		m_max_bound;

	Closed_List_Type*			m_closed_goal_states;

	// sketch related information
	const Sketch_STRIPS_Problem* m_sketch_problem;
	dlplan::policy::Policy m_sketch;
	dlplan::evaluator::EvaluationCache m_evaluation_cache;

    State* m_lapkt_initial_state;
	dlplan::evaluator::EvaluationContext* m_initial_state_context;
	std::vector<std::shared_ptr<const dlplan::policy::Rule>> m_rules;

	std::string m_key_applied_rule;
};

}

}



#endif // Sketch_siw.hxx
