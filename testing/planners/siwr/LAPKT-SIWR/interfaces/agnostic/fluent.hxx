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

#ifndef __FLUENT__
#define __FLUENT__

#include <types.hxx>
#include <strips_prob.hxx>

namespace aptk
{

class Fluent
{
public:

	Fluent( STRIPS_Problem& p );
	~Fluent();

	unsigned	index() const;
	bool		negated() const;

	const std::string&	signature() const;
	const std::string&	pddl_predicate_name() const;
	const Name_Vec&   pddl_obj_names() const;

	void		set_index( unsigned idx );
	void		set_negated( bool negated );
	void		set_signature( const std::string& signature );
	void		set_predicate_name ( const std::string& predicate_name );
	void		set_objs_names ( const Name_Vec& objs_names );

	STRIPS_Problem& problem();

protected:
	STRIPS_Problem&			m_problem;

	// grounded information
	unsigned			m_index;
	bool				m_negated;

    // human readable information
    std::string			m_signature;
	std::string			m_predicate_name;
    Name_Vec			m_objs_names;
};

inline unsigned		Fluent::index() const
{
	return m_index;
}

inline bool		Fluent::negated() const
{
	return m_negated;
}

inline const std::string& Fluent::signature() const
{
	return m_signature;
}

inline const std::string& Fluent::pddl_predicate_name() const {
    return m_predicate_name;
}

inline const Name_Vec& Fluent::pddl_obj_names() const {
    return m_objs_names;
}

inline void	Fluent::set_index( unsigned idx )
{
	m_index = idx;
}

inline void	Fluent::set_negated( bool negated )
{
	m_negated = negated;
}

inline void	Fluent::set_signature( const std::string& sig )
{
	m_signature = sig;
}

inline void Fluent::set_predicate_name ( const std::string& predicate_name )
{
    m_predicate_name = predicate_name;
}

inline void Fluent::set_objs_names ( const Name_Vec& objs_names)
{
    m_objs_names = move(objs_names);
}

}

#endif // Fluent.hxx
