
#include <fs/core/utils/printers/registry.hxx>
#include <fs/core/utils/printers/printers.hxx>
#include <fs/core/constraints/registry.hxx>


namespace fs0::print {


std::ostream& logical_registry::print(std::ostream& os) const {
	
	os  << std::endl << "Component Repository";
	os  << std::endl << "--------------------" << std::endl;
	os << "Formula creators for symbol names: ";
	for (const auto& it:_registry._formula_creators) {
		os << it.first << ", ";
	}
	os << std::endl << std::endl;
	
	return os;
}



} // namespaces
