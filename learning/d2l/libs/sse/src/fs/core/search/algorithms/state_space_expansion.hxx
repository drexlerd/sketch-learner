
#pragma once

#include <fs/core/utils/system.hxx>
#include <fs/core/problem_info.hxx>

#include <lapkt/algorithms/generic_search.hxx>
#include <lapkt/search/components/open_lists.hxx>
#include <lapkt/search/components/stl_unordered_map_closed_list.hxx>
#include <lapkt/tools/resources_control.hxx>
#include <random>


namespace fs0::algorithms {

//! Partial specialization of the GenericSearch algorithm:
//! A breadth-first search is a generic search with a FIFO open list and 
//! a standard unsorted closed list. Type of node and state model are still generic.
template <typename NodeT,
          typename StateModel,
          typename StatsT
>
class StateSpaceExpansion {
public:
    using OpenListT = lapkt::SimpleQueue<NodeT>;
    using ClosedListT = aptk::StlUnorderedMapClosedList<NodeT>;
    using StateT = typename StateModel::StateT;
    using ActionIdT = typename StateModel::ActionType::IdType;
    using PlanT =  std::vector<ActionIdT>;
    using NodePT = std::shared_ptr<NodeT>;


	//! The constructor requires the user of the algorithm to inject both
	//! (1) the state model to be used in the search
	//! (2) the particular open and closed list objects
    StateSpaceExpansion(
        const StateModel& model,
        StatsT& stats,
        long max_expansions,
        long max_nodes_per_class,
        bool ignore_non_fringe_dead_states,
        bool print_transitions,
        bool stop_on_goal,
        bool verbose,
        unsigned seed)
        : _model(model),
          _open(),
          _closed(),
          _stats(stats),
          _max_expansions(max_expansions),
          _max_nodes_per_class(max_nodes_per_class),
          _ignore_non_fringe_dead_states(ignore_non_fringe_dead_states),
          _print_transitions(print_transitions),
          _stop_on_goal(stop_on_goal),
          _verbose(verbose),
          _seed(seed)
	{}

	virtual ~StateSpaceExpansion() = default;
	
	// Disallow copy, but allow move
	StateSpaceExpansion(const StateSpaceExpansion&) = delete;
	StateSpaceExpansion(StateSpaceExpansion&&) noexcept = default;
	StateSpaceExpansion& operator=(const StateSpaceExpansion&) = delete;
	StateSpaceExpansion& operator=(StateSpaceExpansion&&) noexcept = default;

    float node_generation_rate() {
        return _stats.generated() * 1.0 / (aptk::time_used() - _stats.initial_search_time());
    }

	void on_generation(const NodeT& node) {
        _stats.generation(node.g);

        if (_verbose) {
            auto generated = _stats.generated();
            if (generated % 50000 == 0) {
                LPT_INFO("cout", "Node generation rate after " << generated / 1000 << "K generations (nodes/sec.): " << node_generation_rate()
                                                               << ". Memory consumption: "<< fs0::get_current_memory_in_kb() << "kB. / " << fs0::get_peak_memory_in_kb() << " kB.");
            }
        }
	}

    //! Convenience method
    bool solve_model(PlanT& solution) { return search( _model.init(), solution ); }

    void log_generated_node(NodeT& n, bool is_goal, bool deadend) {
        const auto& info = fs0::ProblemInfo::getInstance();

        char code = 'A';  // "Alive"
        if (deadend) code = 'D';
        else if (is_goal) code = 'G';


        std::cout << "(N) " << n.id << " " << code << " ";
        // THIS IS COPY-PASTED FROM THE STATE PRINTER
        const auto& s = n.state;
        bool something_already_printed = false;
        for (unsigned x = 0; x < info.getNumVariables(); ++x) {
            fs0::object_id o = s.getValue(x);
            std::string atom;

            if (fs0::o_type(o) == fs0::type_id::bool_t) {
                if (fs0::value<bool>(o)) {
                    atom = info.getVariableName(x); // print positive atoms only
                }
            } else {
                atom = info.getVariableName(x) + "=";
                if (fs0::o_type(o) == fs0::type_id::invalid_t) atom += "<invalid>";
                else atom += info.object_name(o);
            }

            if (!atom.empty()) {
                if (something_already_printed) std::cout << " ";
                std::cout << atom;
                something_already_printed = true;
            }
        }
        std::cout << std::endl;
    }

    void log_edge(unsigned parent_id, unsigned child_id) const {
        std::cout << "(E) " << parent_id << " " << child_id << std::endl;
    }

    bool search(const StateT& s, PlanT& solution) {
        std::vector<unsigned> all_goals;
        std::vector<std::vector<unsigned>> parents;
        std::vector<std::vector<unsigned>> children;
        unsigned node_id = 0;

        const auto n = std::make_shared<NodeT>(s, node_id++, 0);
        std::cout << "Exploring state space. "
                  << "stop_on_goal=" << _stop_on_goal
                  << ", max_expansions=" << _max_expansions
                  << ", max_nodes_per_class=" << _max_nodes_per_class
                  << ", ignore_non_fringe_dead_states=" << _ignore_non_fringe_dead_states
                  << ", print_transitions=" << _print_transitions
                  << ", seed=" << _seed
                  << std::endl;

        if (_model.goal(n->state)) all_goals.push_back(n->id);

        this->_open.insert(n);
        _closed.put(n);

        while (!this->_open.empty() && (_max_expansions < 0 || _stats.expanded() < (unsigned) _max_expansions)) {
            NodePT current = this->_open.next();

            _stats.expansion();

            if (children.size() <= current->id) children.resize(current->id+1);
            for (const auto& a : this->_model.applicable_actions(current->state)) {
                NodePT successor = std::make_shared<NodeT>(this->_model.next(current->state, a), node_id++, current->g+1);
                on_generation(*successor);

                auto repeated = _closed.seek(successor);
                if (repeated != nullptr) { // The node has already been closed
                    register_parenthood(repeated->id, current->id, parents);
                    children.at(current->id).push_back(repeated->id);
                    node_id--; // move the ID one back to achieve contiguous IDs
                    continue;
                }

                register_parenthood(successor->id, current->id, parents);
                children.at(current->id).push_back(successor->id);

                // Otherwise, we have a new node:
                if (_model.goal(successor->state)) all_goals.push_back(successor->id);
                this->_open.insert(successor);
                _closed.put(successor);
            }
        }

        if (!_open.empty()) {
            std::cout << "Unable to fully explore state space with max_expansions: " << _max_expansions << std::endl;
            return false;
        }

        const auto num_nodes = _closed.size();
        assert(num_nodes == _stats.expanded());
        assert(num_nodes == node_id);
        assert(num_nodes == parents.size());

        // Compute which nodes are backwards-reachable from some goal, i.e. are not dead
        std::vector<bool> backwards_reachable(num_nodes, false);
        std::vector<bool> goals(num_nodes, false);
        std::queue<unsigned> queue;
        for (const auto g:all_goals) {
            backwards_reachable.at(g) = true;
            goals.at(g) = true;
            queue.push(g);
        }

        while(!queue.empty()) {
            const auto sid = queue.front();
            queue.pop();
            const auto& parents_s = parents.at(sid);
            for (const auto p:parents_s) {
                if (!backwards_reachable.at(p)) {
                    backwards_reachable.at(p) = true;
                    queue.push(p);
                }
            }
        }

        unsigned dead_not_on_fringe = 0;

        // If the user wants only some sample of states for each class solvable/unsolvable, we shuffle the nodes here
        std::vector<NodePT> shuffled(_closed.begin(), _closed.end());
        if (_max_nodes_per_class>0) {
            auto rng = std::default_random_engine{_seed};
            std::shuffle(std::begin(shuffled), std::end(shuffled), rng);
        }

        // Output the shuffled nodes, up to a limit, if specified
        unsigned printed_unsolvable = 0, printed_solvable = 0;
        std::cout << std::endl  << std::endl << "== GENERATED NODES ==" << std::endl;
        for (const auto& node:shuffled) {
            if (_max_nodes_per_class>0 && printed_unsolvable >=_max_nodes_per_class && printed_solvable>=_max_nodes_per_class) {
                break;
            }

            bool unsolvable = !backwards_reachable[node->id];
            bool is_goal = goals[node->id];

            // Skip the state if we're ignoring non-fringe dead states and the state is one of these.
            if (_ignore_non_fringe_dead_states && unsolvable) {
                const auto& parents_s = parents.at(node->id);
                bool has_alive_parent = std::any_of(parents_s.begin(), parents_s.end(), [&backwards_reachable,&goals](unsigned par){
                  return backwards_reachable[par] && !goals[par];
                });

                if (!has_alive_parent) {
                    dead_not_on_fringe++;
                    continue;
                }
            }

            if (_max_nodes_per_class>0 && unsolvable && printed_unsolvable >= _max_nodes_per_class) {
                continue;
            }
            if (_max_nodes_per_class>0 && !unsolvable && printed_solvable >= _max_nodes_per_class) {
                continue;
            }

            log_generated_node(*node, is_goal, unsolvable);
            if (_print_transitions) {
                for (unsigned cid:children.at(node->id)) {
                    log_edge(node->id, cid);
                }
            }

            if (unsolvable) printed_unsolvable++;
            else printed_solvable++;
        }

        // Print summary line
        auto num_solvable = std::count(backwards_reachable.begin(), backwards_reachable.end(), true);
        unsigned num_dead = _stats.expanded() - num_solvable;
        unsigned dead_on_fringe = num_dead - dead_not_on_fringe;

        std::cout << std::endl << "== STATE SPACE EXPANDED (states:" << _stats.expanded()
                  //                  << ", transitions: " << _stats.generated()
                  << ", solvable: " << num_solvable
                  << ", dead: " << num_dead
                  << ", dead-on-fringe: " << dead_on_fringe
                  << ", goals:" << all_goals.size() << ") =="
                  << std::endl << std::endl;

        return false;
    }

    void register_parenthood(unsigned child, unsigned parent, std::vector<std::vector<unsigned>>& parents) const {
        if (parents.size() <= child) parents.resize(child+1);
        parents[child].push_back(parent);
    }

protected:
    //! The search model
    const StateModel& _model;

    //! The open list
    OpenListT _open;

    //! The closed list
    ClosedListT _closed;

    StatsT& _stats;

    long _max_expansions;

    //! How many nodes at most we want to print for each class (solvable, unsolvable)
    long _max_nodes_per_class;

    //! Whether to ignore those dead states that are not on the fringe. A dead state is "on the fringe" if
    //! it is the successor of at least one alive state.
    bool _ignore_non_fringe_dead_states;

    //! Whether to print state space transitions
    bool _print_transitions;

    bool _stop_on_goal;

    bool _verbose;

    //! The seed for the RNG used to randomize the printed nodes of each class, if necessary
    unsigned _seed;
}; 

}
