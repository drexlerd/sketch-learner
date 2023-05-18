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

#include <sketch_strips_prob.hxx>
#include <action.hxx>
#include <fluent.hxx>
#include <cassert>
#include <map>
#include <iostream>
#include <unordered_map>


namespace aptk
{
	Sketch_STRIPS_Problem::Sketch_STRIPS_Problem( std::string dom_name, std::string prob_name )
		: STRIPS_Problem(dom_name, prob_name),
		m_num_static_fluents(0),
		m_num_total_fluents(0),
		m_num_predicates(0),
		m_num_objects(0) {
		m_vocabulary_info = std::make_shared<dlplan::core::VocabularyInfo>();
		m_instance_info = std::make_shared<dlplan::core::InstanceInfo>(m_vocabulary_info);
	}

	Sketch_STRIPS_Problem::~Sketch_STRIPS_Problem()
	{
	}

	void Sketch_STRIPS_Problem::set_goal( const Fluent_Vec& goal_vec )
	{
		if ( m_in_goal.empty() )
			m_in_goal.resize( num_fluents(), false );
		else
			for ( unsigned k = 0; k < num_fluents(); k++ )
				m_in_goal[k] = false;

		goal().assign( goal_vec.begin(), goal_vec.end() );

		for ( unsigned k = 0; k < goal_vec.size(); k++ )
			m_in_goal[ goal_vec[k] ] = true;

        // Initialize dlplan related stuff
		// add goal versions
		for (unsigned goal_fluent_idx : goal_vec) {
			Fluent* goal_fluent = fluents()[goal_fluent_idx];
			const std::string& predicate_name = goal_fluent->pddl_predicate_name() + "_g";
			dlplan::core::Atom static_dlplan_atom = m_instance_info->add_static_atom(predicate_name, goal_fluent->pddl_obj_names());
			m_static_dlplan_atoms.push_back(static_dlplan_atom);
		}
	}

	unsigned Sketch_STRIPS_Problem::add_fluent( std::string signature, std::string predicate_name, Name_Vec &&objs_names, bool negated )
	{
		assert(m_static_fluents.empty());

		Fluent* new_fluent = new Fluent( *this );
		new_fluent->set_index( fluents().size() );
		new_fluent->set_signature( signature );
		new_fluent->set_negated( negated );
		new_fluent->set_predicate_name(predicate_name);
		new_fluent->set_objs_names(objs_names);

		dlplan::core::Atom dlplan_atom = m_instance_info->add_atom(predicate_name, objs_names);
		m_dlplan_atoms.push_back(dlplan_atom);

		m_fluents_map[signature] = new_fluent->index();
		increase_num_fluents();
		fluents().push_back( new_fluent );
		m_const_fluents.push_back( new_fluent );
		m_num_total_fluents++;
		m_total_fluents.push_back( new_fluent );
		m_total_const_fluents.push_back( new_fluent );
		return fluents().size()-1;
	}

	unsigned Sketch_STRIPS_Problem::add_static_fluent( std::string signature, std::string predicate_name, Name_Vec &&objs_names, bool negated )
	{
		Fluent* new_fluent = new Fluent( *this );
		new_fluent->set_index( fluents().size() + static_fluents().size() );
		new_fluent->set_signature( signature );
		new_fluent->set_negated( negated );
		new_fluent->set_predicate_name(predicate_name);
		new_fluent->set_objs_names(objs_names);

		dlplan::core::Atom static_dlplan_atom = m_instance_info->add_static_atom(predicate_name, objs_names);
        m_static_dlplan_atoms.push_back(static_dlplan_atom);

		m_num_static_fluents++;
		m_static_fluents.push_back( new_fluent);
		m_static_const_fluents.push_back( new_fluent );
		m_num_total_fluents++;
		m_total_fluents.push_back( new_fluent );
		m_total_const_fluents.push_back( new_fluent );
		return m_static_fluents.size()-1;
	}

	void Sketch_STRIPS_Problem::add_predicate( std::string predicate_name, int arity ) {
        m_vocabulary_info->add_predicate(predicate_name, arity);
		m_vocabulary_info->add_predicate(predicate_name + "_g", arity);
	}

	void Sketch_STRIPS_Problem::add_constant( std::string object_name ) {
		m_vocabulary_info->add_constant(object_name);
	}

	dlplan::core::State Sketch_STRIPS_Problem::from_lapkt_state(State* state, int state_id) const {
		std::vector<int> atom_idxs;
		atom_idxs.reserve(m_num_total_fluents);
		// Add dynamic atoms
		for (unsigned fluent_idx : state->fluent_vec()) {
			if (fluents()[fluent_idx]->negated()) continue;  // we dont use negated fluents in dlplan state
            atom_idxs.push_back(fluent_idx);
		}
		return dlplan::core::State(m_instance_info, atom_idxs, state_id);
	}

	dlplan::core::State Sketch_STRIPS_Problem::get_default_state() const {
		return dlplan::core::State(m_instance_info, std::vector<int>());
	}

	void Sketch_STRIPS_Problem::print_static_fluents( std::ostream& os ) const {
		for ( unsigned k = 0; k < static_fluents().size(); k++ ) {
			os << k+1 << ". " << static_fluents().at(k)->signature() << std::endl;
		}
	}
}
