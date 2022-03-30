
#pragma once

#include <vector>
#include <memory>

#include <fs/core/search/drivers/registry.hxx>
#include <fs/core/search/stats.hxx>
#include <fs/core/models/ground_state_model.hxx>


namespace fs0 { class Config; }

namespace fs0::drivers {


//! An engine to expand entire state spaces
class StateSpaceExpansionDriver : public Driver {
public:
	GroundStateModel setup(Problem& problem) const;

	ExitCode search(Problem& problem, const Config& config, const EngineOptions& options, float start_time) override;

protected:
	SearchStats _stats;
};

} // namespaces
