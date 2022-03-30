
#include <fs/core/languages/fstrips/language.hxx>
#include <fs/core/applicability/formula_interpreter.hxx>
#include <fs/core/languages/fstrips/operations.hxx>
#include <fs/core/utils/utils.hxx>
#include <lapkt/tools/logging.hxx>

namespace fs0 {

FormulaInterpreter* FormulaInterpreter::create(const fs::Formula* formula, const AtomIndex& tuple_index) {
    LPT_INFO("main", "Created a direct sat. manager for formula: " << *formula);
    return new DirectFormulaInterpreter(formula);
}

FormulaInterpreter::FormulaInterpreter(const fs::Formula* formula) :
	_formula(formula->clone())
{}

FormulaInterpreter::~FormulaInterpreter() {
	delete _formula;
}

FormulaInterpreter::FormulaInterpreter(const FormulaInterpreter& other) :
	_formula(other._formula->clone())
{}


bool DirectFormulaInterpreter::satisfied(const State& state) const {
	return _formula->interpret(state);
}

} // namespaces
