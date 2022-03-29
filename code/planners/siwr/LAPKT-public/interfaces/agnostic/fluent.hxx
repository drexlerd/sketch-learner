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

	const std::string&	signature() const;
	const std::string&	pddl_predicate_name() const;

	void		set_index( unsigned idx );
	void		set_negated( bool negated );
	void		set_signature( const std::string& signature );

	STRIPS_Problem& problem();

protected:
	STRIPS_Problem&			m_problem;

	// grounded information
	unsigned			m_index;

    // human readable information
    std::string			m_signature;
};

inline unsigned		Fluent::index() const
{
	return m_index;
}

inline const std::string& Fluent::signature() const
{
	return m_signature;
}

inline void	Fluent::set_index( unsigned idx )
{
	m_index = idx;
}

inline void	Fluent::set_signature( const std::string& sig )
{
	m_signature = sig;
}

}

#endif // Fluent.hxx
