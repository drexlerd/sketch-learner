#ifndef __PY_FOD_PROBLEM__
#define __PY_FOD_PROBLEM__

#include <py_strips_prob.hxx>
#include <sketch_strips_prob.hxx>
#include <fluent.hxx>
#include <action.hxx>
#include <boost/python.hpp>
#include <string>
#include <vector>


class Sketch_STRIPS_Problem : public STRIPS_Problem {
public:
	Sketch_STRIPS_Problem(  );
	Sketch_STRIPS_Problem( std::string, std::string );
	virtual ~Sketch_STRIPS_Problem();

	aptk::Sketch_STRIPS_Problem*	instance() {
		return static_cast<aptk::Sketch_STRIPS_Problem*>(m_problem);
	}

	void set_goal( boost::python::list& list );

    // add atoms that occur in effects of operators.
	void add_atom(
		std::string name, std::string predicate_name, boost::python::list &objects);
    // add atoms that do not occur in effects of operators.
	void add_static_atom(
		std::string name, std::string predicate_name, boost::python::list &objects);

    void add_predicate( std::string predicate_name, int arity );

	void add_constant( std::string object_name );

	void create_negated_fluents_ext();

	void set_sketch_textual( std::string sketch_textual );
};

#endif // py_sketch_strips_problem.hxx
