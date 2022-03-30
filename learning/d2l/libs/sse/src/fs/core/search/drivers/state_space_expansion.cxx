
#include <fs/core/search/drivers/state_space_expansion.hxx>

#include <fs/core/state.hxx>
#include <fs/core/search/nodes/state_space_expansion_node.hxx>
#include <fs/core/search/algorithms/state_space_expansion.hxx>
#include <fs/core/search/utils.hxx>
#include <fs/core/search/drivers/setups.hxx>
#include <fs/core/utils/config.hxx>


namespace fs0::drivers {

GroundStateModel
StateSpaceExpansionDriver::setup(Problem& problem) const {
	return GroundingSetup::fully_ground_model(problem);
}


ExitCode
StateSpaceExpansionDriver::search(Problem& problem, const Config& config, const EngineOptions& options, float start_time) {
	//! The Breadth-First Search engine uses a simple blind-search node
	using NodeT = lapkt::StateSpaceExpansionNode<State>;

    auto model = setup(problem);

    fs0::algorithms::StateSpaceExpansion<NodeT, GroundStateModel, SearchStats> engine(
        model, _stats,
        config.getOption<long>("max_expansions", -1),
        config.getOption<long>("max_nodes_per_class", -1),
        config.getOption<bool>("ignore_non_fringe_dead_states", true),
        config.getOption<bool>("print_transitions", true),
        config.getOption<bool>("until_first_goal", false),
        config.getOption<bool>("verbose_stats", false),
        config.getOption<unsigned>("seed", 1)
    );

	Utils::SearchExecution<GroundStateModel>(model).do_search(engine, options, start_time, _stats);
    return ExitCode::SUCCESS;
}

} // namespaces
