from re import sub
from turtle import color
import dlplan
import logging
import math

from copy import deepcopy
from collections import defaultdict, deque, OrderedDict
from typing import  List, FrozenSet, MutableSet, Dict
from termcolor import colored

from .returncodes import ExitCode
from .util.command import create_experiment_workspace, read_file, write_file
from .domain_data.domain_data_factory import DomainDataFactory
from .instance_data.instance_information import InstanceInformation
from .instance_data.instance_data import InstanceData
from .instance_data.instance_data_factory import InstanceDataFactory
from .instance_data.tuple_graph_factory import TupleGraphFactory
from .iteration_data.sketch import Sketch
from .learning_sketches_step import learn_sketch


def partition_states_by_distance(distances):
    max_distance = max(distances.values())
    s_idxs_by_distance = [[] for _ in range(max_distance + 1)]
    for s_idx, distance in distances.items():
        s_idxs_by_distance[distance].append(s_idx)
    return s_idxs_by_distance


def compute_delta_optimal_states(instance_data: InstanceData, delta: float, s_idx: int, goal_distances: Dict[int, int]):
    state_space = instance_data.state_space
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
        cur_layer = next_layer
    return state_indices


def compute_delta_optimal_subgoal_states(delta: float, instance_data: InstanceData, root_idx: int, rule: dlplan.Rule):
    source_state = instance_data.state_information.get_state(root_idx)
    if not rule.evaluate_conditions(source_state):
        return set()
    forward_successors = instance_data.state_space.get_forward_successor_state_indices()
    layers = [[root_idx]]
    distances = dict()
    distances[root_idx] = 0
    delta_optimal_subgoal_states = set()
    prev_layer = layers[0]
    optimal_distance = None
    while True:
        next_layer = []
        for s_idx in prev_layer:
            for s_prime_idx in forward_successors.get(s_idx, []):
                if distances.get(s_prime_idx, math.inf) == math.inf:
                    next_layer.append(s_prime_idx)
                    distances[s_prime_idx] = distances[s_idx] + 1
                    target_state = instance_data.state_information.get_state(s_prime_idx)
                    if rule.evaluate_effects(source_state, target_state, instance_data.denotations_caches):
                        delta_optimal_subgoal_states.add(s_prime_idx)
        if not next_layer:
            break
        layers.append(next_layer)
        prev_layer = next_layer
        if optimal_distance is None and delta_optimal_subgoal_states:
            optimal_distance = len(layers) - 1
        elif optimal_distance is not None and len(layers) - 1 == delta * optimal_distance:
            break
    return delta_optimal_subgoal_states


def compute_subgoal_class_to_initial_s_idxs(delta: float, instance_data: InstanceData, rule: dlplan.Rule):
    subgoals_class_to_initial_s_idxs = defaultdict(set)
    for s_idx in instance_data.state_space.get_state_indices():
        if not instance_data.goal_distance_information.is_alive(s_idx):
            continue
        closest_subgoal_states = compute_delta_optimal_subgoal_states(delta, instance_data, s_idx, rule)
        if not closest_subgoal_states:
            continue
        subgoals_class_to_initial_s_idxs[tuple(sorted(list(closest_subgoal_states)))].add(s_idx)
    # print("Num subgoal classes:", len(subgoals_class_to_initial_s_idxs))
    # print("Num states:", instance_data.state_space.get_num_states())
    return subgoals_class_to_initial_s_idxs


def compute_initial_states_inducing_largest_subproblems(instance_data: InstanceData, initial_s_idxs: MutableSet[int], subgoals: FrozenSet[int]):
    selected_initial_s_idxs = set()
    layers = partition_states_by_distance(instance_data.goal_distance_information.get_goal_distances())
    marked_initial_s_idxs = set()
    for backward_layer in reversed(layers):
        backward_layer = set(backward_layer)
        for s_idx in backward_layer:
            if s_idx in initial_s_idxs and not s_idx in marked_initial_s_idxs:
                selected_initial_s_idxs.add(s_idx)
                marked_initial_s_idxs.add(s_idx)
            if s_idx in marked_initial_s_idxs:
                for target_idx in instance_data.state_space.get_forward_successor_state_indices().get(s_idx, []):
                    if target_idx not in backward_layer:
                        marked_initial_s_idxs.add(target_idx)
    # print("Subgoal class:", subgoals)
    # print("Num initial states:", len(initial_s_idxs))
    # print("Num initial state classes:", len(selected_initial_s_idxs))
    return selected_initial_s_idxs


def make_subproblems(config, instance_datas: List[InstanceData], sketch: dlplan.Policy, rule: dlplan.Rule):
    features = sketch.get_boolean_features() + sketch.get_numerical_features()
    subproblem_instance_datas = []
    for instance_data in instance_datas:
        state_space = instance_data.state_space
        state_information = instance_data.state_information
        # 1. Compute feature valuations F over Phi for each state
        feature_valuation_to_s_idxs = defaultdict(set)
        for s_idx in state_space.get_state_indices():
            feature_valuation = tuple([feature.evaluate(state_information.get_state(s_idx)) for feature in features])
            feature_valuation_to_s_idxs[feature_valuation].add(s_idx)
        # 2. For each f in F with f satisfies C ...
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
            # 4. Compute delta optimal forward reachable states.
            ordered_initial_s_idxs = [x[0] for x in sorted([(s_idx, goal_distances.get(s_idx)) for s_idx in initial_s_idxs if goal_distances.get(s_idx, math.inf) != math.inf], key=lambda x: x[1])]
            state_indices = set()
            solvable_initial_s_idxs = set()
            for initial_s_idx in ordered_initial_s_idxs:
                solvable_initial_s_idxs.add(initial_s_idx)
                state_indices.update(compute_delta_optimal_states(instance_data, config.delta, initial_s_idx, goal_distances))
            # 6. Instantiate subproblem for initial state and subgoals.
            subproblem_state_space = dlplan.StateSpace(
                instance_data.state_space,
                state_indices,
                state_indices)
            subproblem_state_space.set_goal_state_indices(goal_s_idxs.intersection(state_indices))
            subproblem_goal_distance_information = subproblem_state_space.compute_goal_distance_information()
            if not subproblem_goal_distance_information.is_solvable() or \
                subproblem_goal_distance_information.is_trivially_solvable():
                continue
            name = f"{instance_data.instance_information.name}-{s_idx}"
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
            subproblem_instance_data.initial_s_idxs = solvable_initial_s_idxs
            # 2.2.1. Recompute tuple graph for restricted state space
            subproblem_instance_data.set_tuple_graphs(TupleGraphFactory(width=0).make_tuple_graphs(subproblem_instance_data))
            subproblem_instance_datas.append(subproblem_instance_data)
    return subproblem_instance_datas




    subproblem_instance_datas = sorted(subproblem_instance_datas, key=lambda x : x.state_space.get_num_states())
    for instance_idx, instance_data in enumerate(subproblem_instance_datas):
        instance_data.id = instance_idx
        instance_data.state_space.get_instance_info().set_index(instance_idx)
    print("Number of subproblems:", len(subproblem_instance_datas))
    return subproblem_instance_datas


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
    logging.info(colored(f"..done", "blue", "on_grey"))

    solution_policies = []
    structurally_minimized_solution_policies = []
    empirically_minimized_solution_policies = []
    for rule in sketch.dlplan_policy.get_rules():
        print("Sketch:")
        print(sketch.dlplan_policy.compute_repr())
        print("Sketch rule:", rule.get_index(), rule.compute_repr())

        rule_workspace = config.experiment_dir / "output" / f"rule_{rule.get_index()}"
        create_experiment_workspace(rule_workspace, rm_if_existed=True)
        write_file(rule_workspace / "rule.txt", rule.compute_repr())
        write_file(rule_workspace / "sketch.txt", sketch.dlplan_policy.compute_repr())

        logging.info(colored(f"Initializing Subproblems...", "blue", "on_grey"))
        subproblem_instance_datas = make_subproblems(config, instance_datas, sketch.dlplan_policy, rule)
        if not subproblem_instance_datas:
            print(colored("Sketch rule does not induce any subproblems!", "red", "on_grey"))
            solution_policies.append(None)
            structurally_minimized_solution_policies.append(None)
            empirically_minimized_solution_policies.append(None)
            break
        logging.info(colored(f"..done", "blue", "on_grey"))

        policy, structurally_minimized_policy, empirically_minimized_policy = learn_sketch(config, domain_data, subproblem_instance_datas, config.experiment_dir / "learning" / f"rule_{rule.get_index()}")
        solution_policies.append(policy)
        structurally_minimized_solution_policies.append(structurally_minimized_policy)
        empirically_minimized_solution_policies.append(empirically_minimized_policy)
        write_file(rule_workspace / "policy.txt", policy.dlplan_policy.compute_repr())
        write_file(rule_workspace / "policy_structurally_minimized.txt", structurally_minimized_policy.dlplan_policy.compute_repr())
        write_file(rule_workspace / "policy_empirically_minimized.txt", empirically_minimized_policy.dlplan_policy.compute_repr())
    logging.info(colored("Summary:", "yellow", "on_grey"))
    print("Input sketch:")
    print(sketch.dlplan_policy.compute_repr())
    print("Learned policies by rule:")
    for rule in sketch.dlplan_policy.get_rules():
        print("Rule", rule.get_index(), rule.compute_repr())
        if solution_policies[rule.get_index()] is not None:
            print("Resulting policy:")
            solution_policies[rule.get_index()].print()
        else:
            print("No policy found.")
    print()
    print("Learned structurally minimized policies by rule:")
    for rule in sketch.dlplan_policy.get_rules():
        print("Rule", rule.get_index(), rule.compute_repr())
        if structurally_minimized_solution_policies[rule.get_index()] is not None:
            print("Resulting structurally minimized sketch:")
            structurally_minimized_solution_policies[rule.get_index()].print()
        else:
            print("No policy found.")
    print()
    print("Learned empirically minimized policies by rule:")
    for rule in sketch.dlplan_policy.get_rules():
        print("Rule", rule.get_index(), rule.compute_repr())
        if empirically_minimized_solution_policies[rule.get_index()] is not None:
            print("Resulting empirically minimized sketch:")
            empirically_minimized_solution_policies[rule.get_index()].print()
        else:
            print("No policy found.")
    return ExitCode.Success, None
