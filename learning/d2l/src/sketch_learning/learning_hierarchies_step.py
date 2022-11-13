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
from .util.clock import Clock
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
    fringe_state_indices = set()
    state_indices = set()
    state_indices.add(s_idx)
    optimal_cost = goal_distances.get(s_idx, math.inf)
    assert optimal_cost != math.inf
    delta_optimal_cost = delta * optimal_cost
    queue = deque()
    queue.append(s_idx)
    forward_distances = dict()
    forward_distances[s_idx] = 0
    forward_successors = state_space.get_forward_successor_state_indices()
    while queue:
        source_idx = queue.popleft()
        source_cost = forward_distances.get(source_idx)
        for target_idx in forward_successors.get(source_idx, []):
            if target_idx not in forward_distances:
                forward_distances[target_idx] = source_cost + 1
                target_distance = goal_distances.get(target_idx, math.inf)
                if source_cost + target_distance <= delta_optimal_cost:
                    state_indices.add(target_idx)
                    if target_distance != 0:
                        # not not add states after the goal.
                        queue.append(target_idx)
                else:
                    fringe_state_indices.add(target_idx)
    return state_indices, fringe_state_indices


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
            old_goal_distance_information = instance_data.goal_distance_information
            old_goal_state_indices = instance_data.state_space.get_goal_state_indices()
            instance_data.state_space.set_goal_state_indices(goal_s_idxs)
            instance_data.goal_distance_information = instance_data.state_space.compute_goal_distance_information()
            # largest goal distance of any initial state
            max_distance = 0
            for initial_s_idx in initial_s_idxs:
                distance = instance_data.goal_distance_information.get_goal_distances().get(initial_s_idx, math.inf)
                if distance > max_distance and distance != math.inf:
                    max_distance = distance
            for initial_s_idx in initial_s_idxs:
                name = f"{instance_data.instance_information.name}-{initial_s_idx}"
                distance = instance_data.goal_distance_information.get_goal_distances().get(initial_s_idx, math.inf)
                if distance != max_distance:
                    continue
                state_indices, fringe_state_indices = compute_delta_optimal_states(instance_data, config.delta, initial_s_idx, instance_data.goal_distance_information.get_goal_distances())
                fringe_state_indices.update(state_indices)
                # 6. Instantiate subproblem for initial state and subgoals.
                subproblem_state_space = dlplan.StateSpace(
                    instance_data.state_space,
                    state_indices,
                    fringe_state_indices)
                subproblem_state_space.set_initial_state_index(initial_s_idx)
                subproblem_state_space.set_goal_state_indices(goal_s_idxs.intersection(state_indices).difference(global_deadends))
                subproblem_goal_distance_information = subproblem_state_space.compute_goal_distance_information()
                if not subproblem_goal_distance_information.is_solvable():
                    continue
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
                subproblem_instance_data.initial_s_idxs = [s_idx for s_idx in state_indices if s_idx in initial_s_idxs]
                # 2.2.1. Recompute tuple graph for restricted state space
                subproblem_instance_data.set_tuple_graphs(TupleGraphFactory(width=0).make_tuple_graphs(subproblem_instance_data))
                subproblem_instance_datas.append(subproblem_instance_data)
            instance_data.state_space.set_goal_state_indices(old_goal_state_indices)
            instance_data.goal_distance_information = old_goal_distance_information
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
        domain_data.zero_cost_boolean_features.add_feature(Feature(boolean_feature, 1))
    for numerical_feature in sketch.dlplan_policy.get_numerical_features():
        domain_data.zero_cost_numerical_features.add_feature(Feature(numerical_feature, 1))


def run(config, data, rng):
    preprocessing_clock = Clock("PREPROCESSING")
    preprocessing_clock.set_start()
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
    preprocessing_clock.set_end()

    num_subproblems_by_rule = []
    num_selected_training_instances_by_rule = []
    sum_num_states_in_selected_training_instances_by_rule = []
    max_num_states_in_selected_training_instances_by_rule = []
    num_features_in_pool_by_rule = []

    learning_clock = Clock("LEARNING")
    learning_clock.set_start()
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
        num_subproblems_by_rule.append(len(subproblem_instance_datas))
        if not subproblem_instance_datas:
            print(colored("Sketch rule does not induce any subproblems!", "red", "on_grey"))
            break
        logging.info(colored(f"..done", "blue", "on_grey"))

        policy, policy_minimized, num_selected_training_instances, sum_num_states_in_selected_training_instances, max_num_states_in_selected_training_instances, num_features_in_pool = learn_sketch(config, domain_data, subproblem_instance_datas, config.experiment_dir / "learning" / f"rule_{rule.get_index()}")
        add_zero_cost_features(domain_data, policy)
        num_selected_training_instances_by_rule.append(num_selected_training_instances)
        sum_num_states_in_selected_training_instances_by_rule.append(sum_num_states_in_selected_training_instances)
        max_num_states_in_selected_training_instances_by_rule.append(max_num_states_in_selected_training_instances)
        num_features_in_pool_by_rule.append(num_features_in_pool)

        rule_hierarchical_sketch.add_child(policy, f"rule_0")
        rule_hierarchical_sketch_minimized.add_child(policy_minimized, f"rule_0")
    learning_clock.set_end()

    logging.info(colored("Summary:", "yellow", "on_grey"))
    logging.info(colored("Hierarchical sketch:", "green", "on_grey"))
    hierarchical_sketch.print()
    logging.info(colored("Hierarchical sketch minimized:", "green", "on_grey"))
    hierarchical_sketch_minimized.print()

    print("Number of subproblems by rule:", num_subproblems_by_rule)
    print("Sum of number of subproblems by rule:", sum(num_subproblems_by_rule))

    print("Number of selected training instances by rule:", num_selected_training_instances_by_rule)
    print("Sum of number of states in selected training instances by rule:", sum_num_states_in_selected_training_instances_by_rule)
    print("Max of number of states in selected training instances by rule:", max_num_states_in_selected_training_instances_by_rule)
    print("Number of features in the pool by rule:", num_features_in_pool_by_rule)

    print("Max of number of selected training instances by rule:", max(num_selected_training_instances_by_rule))
    print("Max of sum of number of states in selected training instances by rule:", max(sum_num_states_in_selected_training_instances_by_rule))
    print("Max of max of number of states in selected training instances by rule:", max(max_num_states_in_selected_training_instances_by_rule))
    print("Max of number of features in the pool by rule:", max(num_features_in_pool_by_rule))

    preprocessing_clock.print()
    learning_clock.print()
    return ExitCode.Success, None
