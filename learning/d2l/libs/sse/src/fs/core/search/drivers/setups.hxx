
#pragma once

#include <fs/core/models/ground_state_model.hxx>

namespace fs0 { class Problem; }

namespace fs0::drivers {

//! A catalog of common setups for grounding actions for both search and heuristic computations.
class GroundingSetup {
public:
	//! A simple model with all grounded actions
	static GroundStateModel fully_ground_model(Problem& problem);
};

} // namespaces
