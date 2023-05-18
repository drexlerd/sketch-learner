#include <py_sketch_strips_prob.hxx>
#include <cstring>
#include <fstream>
#include <iostream>

using namespace boost::python;

	Sketch_STRIPS_Problem::Sketch_STRIPS_Problem( ) {
		m_parsing_time = 0.0f;
		m_ignore_action_costs = false;
		m_problem = new aptk::Sketch_STRIPS_Problem;

	}

	Sketch_STRIPS_Problem::Sketch_STRIPS_Problem( std::string domain, std::string instance ) {
		m_parsing_time = 0.0f;
		m_ignore_action_costs = false;
		m_problem = new aptk::Sketch_STRIPS_Problem( domain, instance );

	}

	Sketch_STRIPS_Problem::~Sketch_STRIPS_Problem() {
	}

	void
	Sketch_STRIPS_Problem::set_goal( boost::python::list& lits ) {
		aptk::Fluent_Vec G;

		for( int i = 0; i < len(lits); i++ ) {
			boost::python::tuple li = extract< tuple >( lits[i] );
			int 	fl_idx 		= extract<int>(li[0]);
			bool	negated 	= extract<bool>(li[1]);
			if ( negated ) {
				assert( m_negated[fl_idx] );
				G.push_back( m_negated[fl_idx]->index() );
				continue;
			}
			G.push_back( fl_idx );
		}
		instance()->set_goal( G );
	}

	void
	Sketch_STRIPS_Problem::add_atom( std::string name, std::string predicate_name, boost::python::list &objects) {
		aptk::Name_Vec objs_names;
		objs_names.reserve(len(objects));
		for ( int i = 0; i < len(objects); i++ ) {
			std::string obj_name = extract<std::string >( objects[i] );
			objs_names.emplace_back(obj_name);
		}
        instance()->add_fluent( name, predicate_name, move(objs_names), false );
	}

	void
	Sketch_STRIPS_Problem::add_static_atom( std::string name, std::string predicate_name, boost::python::list &objects) {
		aptk::Name_Vec objs_names;
		objs_names.reserve(len(objects));
		for ( int i = 0; i < len(objects); i++ ) {
			std::string obj_name = extract< std::string >( objects[i] );
			objs_names.emplace_back(obj_name);
		}
        instance()->add_static_fluent( name, predicate_name, move(objs_names), false );
	}

	void Sketch_STRIPS_Problem::add_predicate( std::string predicate_name, int arity ) {
        instance()->add_predicate(predicate_name, arity);
	}

	void Sketch_STRIPS_Problem::add_constant( std::string object_name ) {
        instance()->add_constant(object_name);
	}

	void
	Sketch_STRIPS_Problem::create_negated_fluents_ext() {
		m_negated.resize( instance()->num_fluents() );
		unsigned count = 0;
		for ( auto fl_idx : m_negated_conditions ) {
			aptk::Fluent* fl = instance()->fluents()[fl_idx];
			assert( fl != nullptr );
			std::string negated_signature = "(not " + fl->signature() + ")";
			std::vector<std::string> objs_names = fl->pddl_obj_names();
			std::cout << negated_signature << std::endl;
			unsigned neg_fl_idx = instance()->add_fluent( negated_signature, fl->pddl_predicate_name(), move(objs_names), true );
			m_negated.at( fl_idx ) = instance()->fluents()[neg_fl_idx];
			count++;
		}
		std::cout << count << " negated fluents created" << std::endl;
	}

	void Sketch_STRIPS_Problem::set_sketch_textual( std::string sketch_textual ) {
        instance()->set_sketch_textual( sketch_textual );
	}
