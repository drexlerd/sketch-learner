
#pragma once

#include <lapkt/tools/logging.hxx>

namespace lapkt {

template <typename StateT>
class StateSpaceExpansionNode {
public:
    unsigned id;
    
	StateT state;
	
	unsigned g;

	StateSpaceExpansionNode() = delete;
	~StateSpaceExpansionNode() = default;
	
	StateSpaceExpansionNode(const StateSpaceExpansionNode&) = delete;
	StateSpaceExpansionNode(StateSpaceExpansionNode&&) = delete;
	StateSpaceExpansionNode& operator=(const StateSpaceExpansionNode&) = delete;
	StateSpaceExpansionNode& operator=(StateSpaceExpansionNode&&) = delete;
	
	StateSpaceExpansionNode(const StateT& s, unsigned id, unsigned g)
		: StateSpaceExpansionNode(StateT(s), id, g)
	{}

    StateSpaceExpansionNode(StateT&& s, unsigned id, unsigned g)
        : id(id), state(std::move(s)), g(g)
    {}


    //! Print the node into the given stream
	friend std::ostream& operator<<(std::ostream &os, const StateSpaceExpansionNode<StateT>& object) { return object.print(os); }
	std::ostream& print(std::ostream& os) const { 
		os << "{@ = " << this << ", s = " << state << "}";
		return os;
	}

	bool operator==( const StateSpaceExpansionNode<StateT>& o) const { return state == o.state; }

	std::size_t hash() const { return state.hash(); }
};

}  // namespaces
