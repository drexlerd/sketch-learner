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
        # We consider feature valuations of all states: solvable and unsolvable, goals and nongoals
        # to be able to instantiate subproblems with all of them.
        feature_valuation_to_s_idxs = defaultdict(set)
        for s_idx in state_space.get_state_indices():
            feature_valuation = tuple([feature.evaluate(state_information.get_state(s_idx)) for feature in features])
            feature_valuation_to_s_idxs[feature_valuation].add(s_idx)
        # 2. For each f in F with f satisfies C ...
        global_deadends = goal_distance_information.get_deadend_state_indices()
        covered_initial_s_idxs = set()
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
            # sort initial states by distance
            sorted_initial_s_idxs = sorted(initial_s_idxs, key=lambda x : -instance_data.goal_distance_information.get_goal_distances().get(x, math.inf))
            for initial_s_idx in sorted_initial_s_idxs:
                if initial_s_idx in covered_initial_s_idxs:
                    continue
                if not instance_data.goal_distance_information.is_alive(initial_s_idx):
                    continue
                name = f"{instance_data.instance_information.name}-{initial_s_idx}"
                state_indices, fringe_state_indices = compute_delta_optimal_states(instance_data, config.delta, initial_s_idx, instance_data.goal_distance_information.get_goal_distances())
                state_indices_opt, fringe_state_indices_opt = compute_delta_optimal_states(instance_data, 1, initial_s_idx, instance_data.goal_distance_information.get_goal_distances())

                subproblem_initial_s_idxs = set()
                for initial_s_prime_idx in initial_s_idxs:
                    if initial_s_prime_idx in state_indices_opt:
                        if initial_s_prime_idx in goal_s_idxs:
                            continue
                        subproblem_initial_s_idxs.add(initial_s_prime_idx)
                assert initial_s_idx in subproblem_initial_s_idxs
                covered_initial_s_idxs.update(subproblem_initial_s_idxs)
                # 6. Instantiate subproblem for initial state and subgoals.
                subproblem_state_space = dlplan.StateSpace(
                    instance_data.state_space,
                    state_indices,
                    state_indices.union(fringe_state_indices))
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
                subproblem_instance_data.initial_s_idxs = subproblem_initial_s_idxs
                # subproblem_instance_data.initial_s_idxs = [s_idx for s_idx in state_indices if s_idx in initial_s_idxs]
                # 2.2.1. Recompute tuple graph for restricted state space
                subproblem_instance_data.set_tuple_graphs(TupleGraphFactory(width=0).make_tuple_graphs(subproblem_instance_data))
                subproblem_instance_datas.append(subproblem_instance_data)
            instance_data.state_space.set_goal_state_indices(old_goal_state_indices)
            instance_data.goal_distance_information = old_goal_distance_information
        print("covered initial states", len(covered_initial_s_idxs))
        print(instance_data.state_space.get_num_states())
        print(instance_data.state_space.get_goal_state_indices())
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

def compute_smallest_unsolved_instance(config, sketch: Sketch, instance_datas: List[InstanceData]):
    for instance_data in instance_datas:
        if not sketch.solves(config, instance_data):
            return instance_data
    return None


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
    sketch = Sketch(dlplan.PolicyReader().read(config.sketch, domain_data.syntactic_element_factory), config.input_width)
    policy = Sketch(dlplan.PolicyReader().read(config.policy, domain_data.syntactic_element_factory), 0)
    logging.info(colored(f"..done", "blue", "on_grey"))
    preprocessing_clock.set_accumulate()

    for rule in sketch.dlplan_policy.get_rules():
        print("Sketch:")
        print(sketch.dlplan_policy.compute_repr())
        print("Sketch rule:", rule.get_index(), rule.compute_repr())

        logging.info(colored(f"Initializing Subproblems...", "blue", "on_grey"))
        preprocessing_clock.set_start()
        subproblem_instance_datas = make_subproblems(config, instance_datas, sketch.dlplan_policy, rule)

        compute_smallest_unsolved_instance(config, policy, subproblem_instance_datas)

    return ExitCode.Success, None