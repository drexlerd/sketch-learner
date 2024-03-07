
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

#ifndef __SKETCH_STRIPS_PROBLEM__
#define __SKETCH_STRIPS_PROBLEM__

#include <strips_prob.hxx>
#include <strips_state.hxx>
#include <string>
#include <map>
#include <iosfwd>
#include <succ_gen.hxx>
#include <match_tree.hxx>
#include <algorithm>
#include <mutex_set.hxx>
#include <memory>
#include <unordered_map>
#include <unordered_set>

#include "memory.h"

#include <dlplan/core.h>
#include <dlplan/policy.h>


namespace aptk
{

struct StateData {

};

class Sketch_STRIPS_Problem : public STRIPS_Problem {
protected:
	std::shared_ptr<const dlplan::policy::Policy> m_sketch;
    // init_fluents, we assume they are added after fluents
	Fluent_Ptr_Vec m_static_fluents;
	std::vector<const Fluent*> m_static_const_fluents;
	unsigned m_num_static_fluents;
	// all fluents that are ever added to the task
	Fluent_Ptr_Vec m_total_fluents;
	std::vector<const Fluent*> m_total_const_fluents;
	unsigned m_num_total_fluents;

    // the total number of predicates occuring in the instance
	unsigned m_num_predicates;
	// the total number of objects occuring in the instance
	unsigned m_num_objects;

    // Initialize the feature factory.
	std::shared_ptr<dlplan::core::VocabularyInfo> m_vocabulary_info;
	std::shared_ptr<dlplan::core::InstanceInfo> m_instance_info;
	// For transforming LAPKT state to dlplan_state
	std::vector<dlplan::core::Atom> m_dlplan_atoms;
	// Atoms that are part of each dlplan_state
	std::vector<dlplan::core::Atom> m_static_dlplan_atoms;

public:
	Sketch_STRIPS_Problem( std::string dom_name = "Unnamed", std::string prob_name = "Unnamed ");
	virtual ~Sketch_STRIPS_Problem();

    /**
	 * Mark specific fluents as goal fluents.
	 */
	void set_goal(const Fluent_Vec& goal );

    /**
	 * Fluents with additional information about predicate index and object indices.
	 * The order in which fluents are added is important for correct indexing:
	 *   1. dynamic positive fluents
	 *   2. dynamic negated fluents
	 *   3. static fluents
	 */
	// fluents that are changed by actions
	unsigned	add_fluent( std::string signature, std::string predicate_name, Name_Vec &&objs_names, bool negated );
	// fluents that remain constant during planning
	unsigned	add_static_fluent( std::string signature, std::string predicate_name, Name_Vec &&objs_names, bool negated );

	void add_predicate( std::string predicate_name, int arity );

	void add_constant( std::string object_name );

    /**
	 * Convert LAPKT state to dlplan state.
	 */
	dlplan::core::State from_lapkt_state(State* state, int state_id=-1) const;

	dlplan::core::State get_default_state() const;

    /**
	 * Setters
	 */
	void set_sketch_textual( std::string sketch_textual ) {
		auto element_factory = std::make_shared<dlplan::core::SyntacticElementFactory>(m_vocabulary_info);
		dlplan::policy::PolicyFactory policy_factory(element_factory);
		m_sketch = policy_factory.parse_policy(sketch_textual);
	}

    /**
	 * Getters.
	 */
	Fluent_Ptr_Vec& static_fluents() { return m_static_fluents; }
	const std::vector< const Fluent*>& static_fluents() const { return m_static_const_fluents; }
	Fluent_Ptr_Vec& total_fluents() { return m_total_fluents; }
	const std::vector< const Fluent*>& total_fluents() const { return m_total_const_fluents; }

    unsigned num_total_fluents() const { return m_num_total_fluents; }
    unsigned num_predicates() const { return m_num_predicates; }
	unsigned num_objects() const { return m_num_objects; }

	const std::shared_ptr<const dlplan::policy::Policy> sketch() const { return m_sketch; }

    /**
	 * Printers.
	 */
	void print_static_fluents( std::ostream& os ) const;
};

}

#endif // Sketch_STRIPS_Problem.hxx
