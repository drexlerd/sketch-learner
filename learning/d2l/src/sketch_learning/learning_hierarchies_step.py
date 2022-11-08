from re import sub
from turtle import color
import dlplan
import logging
import math

from copy import deepcopy
from collections import defaultdict, deque
from typing import  List, Dict
from termcolor import colored

from .returncodes import ExitCode
from .util.command import create_experiment_workspace, read_file, write_file
from .domain_data.domain_data_factory import DomainDataFactory
from .instance_data.instance_information import InstanceInformation
from .instance_data.instance_data import InstanceData
from .instance_data.instance_data_factory import InstanceDataFactory
from .instance_data.tuple_graph_factory import TupleGraphFactory
from .iteration_data.sketch import Sketch
from .iteration_data.hierarchical_sketch import HierarchicalSketch
from .iteration_data.domain_feature_data import Features, Feature
from .learning_sketches_step import learn_sketch


def compute_delta_optimal_states(instance_data: InstanceData, delta: float, s_idx: int, goal_distances: Dict[int, int]):
    state_space = instance_data.state_space
    state_indices_generated = set()
    state_indices = set()
    state_indices.add(s_idx)
    optimal_cost = goal_distances.get(s_idx, math.inf)
    assert optimal_cost != math.inf
    delta_optimal_cost = delta * optimal_cost
    visited = set()
    cur_layer = set()
    visited.add(s_idx)
    cur_layer.add(s_idx)
    forward_successors = state_space.get_forward_successor_state_indices()
    distance = 0
    while cur_layer:
        distance += 1
        next_layer = set()
        for s_idx in cur_layer:
            for s_prime_idx in forward_successors.get(s_idx, []):
                if s_prime_idx not in visited:
                    visited.add(s_prime_idx)
                    if distance + goal_distances.get(s_prime_idx, math.inf) <= delta_optimal_cost:
                        state_indices.add(s_prime_idx)
                        # Ensure that states are excluded that are only reachable through goal states.
                        if goal_distances.get(s_prime_idx, math.inf) != 0:
                            next_layer.add(s_prime_idx)
                    else:
                        state_indices_generated.add(s_prime_idx)
        cur_layer = next_layer
    state_indices_generated.update(state_indices)
    return state_indices, state_indices_generated


def make_subproblems(config, instance_datas: List[InstanceData], sketch: dlplan.Policy, rule: dlplan.Rule):
    features = sketch.get_boolean_features() + sketch.get_numerical_features()
    subproblem_instance_datas = []
    for instance_data in instance_datas:
        state_space = instance_data.state_space
        goal_distance_information = instance_data.goal_distance_information
        state_information = instance_data.state_information
        # 1. Compute feature valuations F over Phi for each state
        feature_valuation_to_s_idxs = defaultdict(set)
        for s_idx in state_space.get_state_indices():
            if goal_distance_information.is_deadend(s_idx):
                # Ignore deadends from original instance as potential initial states
                continue
            feature_valuation = tuple([feature.evaluate(state_information.get_state(s_idx)) for feature in features])
            feature_valuation_to_s_idxs[feature_valuation].add(s_idx)
        # 2. For each f in F with f satisfies C ...
        global_deadends = goal_distance_information.get_deadend_state_indices()
        for _, initial_s_idxs in feature_valuation_to_s_idxs.items():
            # 2.1. Compute set of initial states, i.e., all s such that f(s) = f,
            if not rule.evaluate_conditions(state_information.get_state(next(iter(initial_s_idxs))), instance_data.denotations_caches):
                continue
            # 2.2. Compute set of goal states, i.e., all s' such that (f(s), f(s')) satisfies E.
            goal_s_idxs = set()
            for _, target_s_idxs in feature_valuation_to_s_idxs.items():
                if not rule.evaluate_effects(state_information.get_state(next(iter(initial_s_idxs))), state_information.get_state(next(iter(target_s_idxs))), instance_data.denotations_caches):
                    continue
                goal_s_idxs.update(target_s_idxs)
            if not goal_s_idxs:
                continue
            # 3. Compute goal distances of all initial states.
            # Do backward search from goal states until all initial states are reached.
            queue = deque()
            goal_distances = dict()
            for s_idx in goal_s_idxs:
                queue.append(s_idx)
                goal_distances[s_idx] = 0
            backward_successors = state_space.get_backward_successor_state_indices()
            unvisited_initial_s_idxs = deepcopy(initial_s_idxs)
            while queue:
                s_idx = queue.popleft()
                s_cost = goal_distances[s_idx]
                if not unvisited_initial_s_idxs:
                    break
                for s_prime_idx in backward_successors.get(s_idx, []):
                    if s_prime_idx not in goal_distances:
                        goal_distances[s_prime_idx] = s_cost + 1
                        queue.append(s_prime_idx)
                    try:
                        unvisited_initial_s_idxs.remove(s_prime_idx)
                    except KeyError:
                        pass
            max_distance_initial_s_idx = None
            max_distance = 0
            for initial_s_idx in initial_s_idxs:
                distance = goal_distances.get(initial_s_idx, math.inf)
                if distance > max_distance and distance != math.inf:
                    max_distance = distance
                    max_distance_initial_s_idx = initial_s_idx
            if max_distance_initial_s_idx is None:
                continue
            initial_s_idx = max_distance_initial_s_idx
            state_indices, state_indices_generated = compute_delta_optimal_states(instance_data, config.delta, initial_s_idx, goal_distances)
            # Collect successor deadends
            forward_successors = state_space.get_forward_successor_state_indices()
            additional_deadends = set()
            for s_idx in state_indices:
                for s_prime_idx in forward_successors.get(s_idx, []):
                    if goal_distance_information.is_deadend(s_prime_idx):
                        additional_deadends.add(s_prime_idx)
            state_indices.update(additional_deadends)
            state_indices_generated.update(additional_deadends)
            # 6. Instantiate subproblem for initial state and subgoals.
            subproblem_state_space = dlplan.StateSpace(
                instance_data.state_space,
                state_indices,
                state_indices_generated)
            subproblem_state_space.set_initial_state_index(initial_s_idx)
            goal_s_idxs.intersection_update(state_indices)
            goal_s_idxs.difference_update(global_deadends)
            subproblem_state_space.set_goal_state_indices(goal_s_idxs)
            subproblem_goal_distance_information = subproblem_state_space.compute_goal_distance_information()
            name = f"{instance_data.instance_information.name}-{initial_s_idx}"
            subproblem_instance_information = InstanceInformation(
                name,
                instance_data.instance_information.filename,
                instance_data.instance_information.workspace / f"rule_{rule.get_index()}" / name)
            subproblem_state_information = subproblem_state_space.compute_state_information()
            subproblem_instance_data = InstanceData(
                len(subproblem_instance_datas),
                instance_data.domain_data,
                instance_data.denotations_caches,
                instance_data.novelty_base,
                subproblem_instance_information)
            subproblem_instance_data.set_state_space(subproblem_state_space)
            subproblem_instance_data.set_goal_distance_information(subproblem_goal_distance_information)
            subproblem_instance_data.set_state_information(subproblem_state_information)
            subproblem_instance_data.initial_s_idxs = {initial_s_idx}
            # 2.2.1. Recompute tuple graph for restricted state space
            subproblem_instance_data.set_tuple_graphs(TupleGraphFactory(width=0).make_tuple_graphs(subproblem_instance_data))
            subproblem_instance_datas.append(subproblem_instance_data)
    subproblem_instance_datas = sorted(subproblem_instance_datas, key=lambda x : x.state_space.get_num_states())
    for instance_idx, instance_data in enumerate(subproblem_instance_datas):
        instance_data.id = instance_idx
        instance_data.state_space.get_instance_info().set_index(instance_idx)
    print("Number of problems:", len(instance_datas))
    print("Number of subproblems:", len(subproblem_instance_datas))
    print("Highest number of states in problem:", max([instance_data.state_space.get_num_states() for instance_data in instance_datas]))
    print("Highest number of states in subproblem:", max([instance_data.state_space.get_num_states() for instance_data in subproblem_instance_datas]))
    return subproblem_instance_datas


def add_zero_cost_features(domain_data, sketch: Sketch):
    for boolean_feature in sketch.dlplan_policy.get_boolean_features():
        domain_data.zero_cost_boolean_features.add_feature(Feature(boolean_feature, 0))
    for numerical_feature in sketch.dlplan_policy.get_numerical_features():
        domain_data.zero_cost_numerical_features.add_feature(Feature(numerical_feature, 0))


def run(config, data, rng):
    logging.info(colored(f"Initializing DomainData...", "blue", "on_grey"))
    domain_data = DomainDataFactory().make_domain_data(config)
    logging.info(colored(f"..done", "blue", "on_grey"))

    logging.info(colored(f"Initializing InstanceDatas...", "blue", "on_grey"))
    instance_datas = InstanceDataFactory().make_instance_datas(config, domain_data)
    logging.info(colored(f"..done", "blue", "on_grey"))

    logging.info(colored(f"Initializing TupleGraphs...", "blue", "on_grey"))
    tuple_graph_factory = TupleGraphFactory(width=0)
    for instance_data in instance_datas:
        instance_data.set_tuple_graphs(tuple_graph_factory.make_tuple_graphs(instance_data))
    logging.info(colored(f"..done", "blue", "on_grey"))

    logging.info(colored(f"Initializing Sketch...", "blue", "on_grey"))
    sketch = Sketch(dlplan.PolicyReader().read("\n".join(read_file(config.sketch_filename)), domain_data.syntactic_element_factory), config.input_width)
    add_zero_cost_features(domain_data, sketch)
    logging.info(colored(f"..done", "blue", "on_grey"))

    hierarchical_sketch = HierarchicalSketch(sketch, config.experiment_dir / "output" / "hierarchical_sketch")
    hierarchical_sketch_minimized = HierarchicalSketch(sketch, config.experiment_dir / "output" / "hierarchical_sketch_minimized")
    for rule in sketch.dlplan_policy.get_rules():
        print("Sketch:")
        print(sketch.dlplan_policy.compute_repr())
        print("Sketch rule:", rule.get_index(), rule.compute_repr())
        rule_policy_builder = dlplan.PolicyBuilder()
        rule.copy_to_builder(rule_policy_builder)
        rule_hierarchical_sketch = hierarchical_sketch.add_child(Sketch(rule_policy_builder.get_result(), sketch.width), f"rule_{rule.get_index()}")
        rule_hierarchical_sketch_minimized = hierarchical_sketch_minimized.add_child(Sketch(rule_policy_builder.get_result(), sketch.width), f"rule_{rule.get_index()}")

        logging.info(colored(f"Initializing Subproblems...", "blue", "on_grey"))
        subproblem_instance_datas = make_subproblems(config, instance_datas, sketch.dlplan_policy, rule)
        if not subproblem_instance_datas:
            print(colored("Sketch rule does not induce any subproblems!", "red", "on_grey"))
            break
        logging.info(colored(f"..done", "blue", "on_grey"))

        policy, policy_minimized = learn_sketch(config, domain_data, subproblem_instance_datas, config.experiment_dir / "learning" / f"rule_{rule.get_index()}")
        add_zero_cost_features(domain_data, policy)

        rule_hierarchical_sketch.add_child(policy, f"rule_0")
        rule_hierarchical_sketch_minimized.add_child(policy_minimized, f"rule_0")
    logging.info(colored("Summary:", "yellow", "on_grey"))
    logging.info(colored("Hierarchical sketch:", "green", "on_grey"))
    hierarchical_sketch.print()
    logging.info(colored("Hierarchical sketch minimized:", "green", "on_grey"))
    hierarchical_sketch_minimized.print()
    return ExitCode.Success, None
