
#include <fs/core/languages/fstrips/scopes.hxx>
#include <fs/core/languages/fstrips/language.hxx>
#include <fs/core/languages/fstrips/operations.hxx>
#include <fs/core/utils/utils.hxx>

namespace fs0::language::fstrips {

std::vector<VariableIdx> ScopeUtils::computeDirectScope(const LogicalElement* element) {
	std::set<VariableIdx> set;
	computeDirectScope(element, set);
	return std::vector<VariableIdx>(set.cbegin(), set.cend());
}

void ScopeUtils::computeDirectScope(const LogicalElement* element, std::set<VariableIdx>& scope) {
	auto state_variables = Utils::filter_by_type<const StateVariable*>(all_nodes(*element));
	for (const StateVariable* sv:state_variables) {
		scope.insert(sv->getValue());
	}
}


} // namespaces
