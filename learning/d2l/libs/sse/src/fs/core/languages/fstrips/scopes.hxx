
#pragma once

#include <fs/core/fs_types.hxx>

namespace fs0 {  class ActionBase; }

namespace fs0::language::fstrips {

class LogicalElement;
class Term;
class Formula;
class ActionEffect;
class FluentHeadedNestedTerm;


//! A number of helper methods to compute and deal with action / formula / term scopes
class ScopeUtils {
public:
	//! Computes the direct scope of a formula or term, i.e. a vector with all state variables involved in the term.
	static std::vector<VariableIdx> computeDirectScope(const LogicalElement* term);
	static void computeDirectScope(const LogicalElement* term, std::set<VariableIdx>& scope);
};

} // namespaces
