#include <siwr_planner.hxx>
using namespace boost::python;

BOOST_PYTHON_MODULE( libsiwr )
{
	class_<SIWR_Planner>("SIWR_Planner")
		.def( init< std::string, std::string >() )
		.def( "add_atom", &SIWR_Planner::add_atom )
		.def( "add_static_atom", &SIWR_Planner::add_static_atom )
		.def( "add_predicate", &SIWR_Planner::add_predicate )
		.def( "add_constant", &SIWR_Planner::add_constant )
		.def( "add_action", &SIWR_Planner::add_action )
		.def( "add_mutex_group", &SIWR_Planner::add_mutex_group )
		.def( "num_atoms", &SIWR_Planner::n_atoms )
		.def( "num_actions", &SIWR_Planner::n_actions )
		.def( "get_atom_name", &SIWR_Planner::get_atom_name )
		.def( "get_domain_name", &SIWR_Planner::get_domain_name )
		.def( "get_problem_name", &SIWR_Planner::get_problem_name )
		.def( "add_precondition", &SIWR_Planner::add_precondition )
		.def( "add_effect", &SIWR_Planner::add_effect )
		.def( "add_cond_effect", &SIWR_Planner::add_cond_effect )
		.def( "set_cost", &SIWR_Planner::set_cost )
		.def( "notify_negated_conditions", &SIWR_Planner::notify_negated_conditions )
		.def( "create_negated_fluents", &SIWR_Planner::create_negated_fluents_ext )
		.def( "set_init", &SIWR_Planner::set_init )
		.def( "set_goal", &SIWR_Planner::set_goal )
		.def( "set_domain_name", &SIWR_Planner::set_domain_name )
		.def( "set_problem_name", &SIWR_Planner::set_problem_name )
		.def( "set_sketch_textual", &Sketch_STRIPS_Problem::set_sketch_textual)
		.def( "write_ground_pddl", &SIWR_Planner::write_ground_pddl )
		.def( "print_action", &SIWR_Planner::print_action )
		.def( "setup", &SIWR_Planner::setup )
		.def( "solve", &SIWR_Planner::solve )
		.def_readwrite( "parsing_time", &SIWR_Planner::m_parsing_time )
		.def_readwrite( "ignore_action_costs", &SIWR_Planner::m_ignore_action_costs )
		.def_readwrite( "iw_bound", &SIWR_Planner::m_iw_bound )
		.def_readwrite( "log_filename", &SIWR_Planner::m_log_filename )
	;
}