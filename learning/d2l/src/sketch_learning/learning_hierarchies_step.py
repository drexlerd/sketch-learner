from re import sub
from turtle import color
import dlplan
import logging

from collections import OrderedDict
from typing import  List
from termcolor import colored

from .instance_data.return_codes import ReturnCode

from .returncodes import ExitCode
from .asp.returncodes import ClingoExitCode
from .util.command import read_file
from .domain_data.domain_data_factory import DomainDataFactory
from .instance_data.instance_data import InstanceData
from .instance_data.instance_data_factory import InstanceDataFactory
from .instance_data.state_pair_classifier import StatePairClassifier
from .instance_data.state_pair_classifier_factory import StatePairClassifierFactory
from .instance_data.tuple_graph_factory import TupleGraphFactory, partition_states_by_distance
from .iteration_data.domain_feature_data_factory import DomainFeatureDataFactory
from .iteration_data.instance_feature_data_factory import InstanceFeatureDataFactory
from .iteration_data.state_pair_equivalence_factory import StatePairEquivalenceFactory
from .iteration_data.dlplan_policy_factory import DlplanPolicyFactory
from .iteration_data.sketch import Sketch, SketchRule
from .asp.policy_asp_factory import PolicyASPFactory
from .util.timer import CountDownTimer
from .learning_sketches_step import learn_sketch


def compute_closest_subgoal_states(instance_data: InstanceData, root_idx: int, rule: SketchRule):
    caches = dlplan.DenotationsCaches()
    source_state = instance_data.state_information.get_state(root_idx)
    if not rule.dlplan_rule.evaluate_conditions(source_state):
        return set()
    distances = instance_data.state_space.compute_distances({root_idx}, True, False)
    layers = partition_states_by_distance(distances)
    for layer in layers:
        closest_subgoal_states = set()
        for target_idx in layer:
            target_state = instance_data.state_information.get_state(target_idx)
            if rule.dlplan_rule.evaluate_effects(source_state, target_state, caches):
                closest_subgoal_states.add(target_idx)
        if closest_subgoal_states:
            return closest_subgoal_states
    return set()


def run(config, data, rng):
    logging.info(colored(f"Initializing DomainData...", "blue", "on_grey"))
    domain_data = DomainDataFactory().make_domain_data(config)
    logging.info(colored(f"..done", "blue", "on_grey"))

    logging.info(colored(f"Initializing InstanceDatas...", "blue", "on_grey"))
    instance_datas = InstanceDataFactory().make_instance_datas(config, domain_data)
    logging.info(colored(f"..done", "blue", "on_grey"))

    logging.info(colored(f"Initializing Sketch...", "blue", "on_grey"))
    sketch = Sketch(dlplan.PolicyReader().read("\n".join(read_file(config.sketch_filename)), domain_data.syntactic_element_factory), config.width)
    logging.info(colored(f"..done", "blue", "on_grey"))

    solution_policies = []
    structurally_minimized_solution_policies = []
    empirically_minimized_solution_policies = []
    for rule in sketch.get_rules():
        print("Sketch:")
        print(sketch.dlplan_policy.compute_repr())
        print("Sketch rule:", rule.dlplan_rule.get_index(), rule.dlplan_rule.compute_repr())

        logging.info(colored(f"Initializing Subproblems...", "blue", "on_grey"))
        subproblem_instance_datas = []
        for instance_data in instance_datas:
            for s_idx in instance_data.state_space.get_state_indices():
                old_initial_state_index = instance_data.state_space.get_initial_state_index()
                old_goal_state_indices = instance_data.state_space.get_goal_state_indices()
                instance_data.state_space.set_initial_state_index(s_idx)
                subgoals = compute_closest_subgoal_states(instance_data, s_idx, rule)
                instance_data.state_space.set_goal_state_indices(subgoals)
                instance_data.state_information = instance_data.state_space.compute_state_information()
                instance_data.goal_distance_information = instance_data.state_space.compute_goal_distance_information()
                instance_data.tuple_graphs = TupleGraphFactory(width=0).make_tuple_graphs(instance_data)
                state_pair_classifier = StatePairClassifierFactory(config.delta).make_state_pair_classifier(config, instance_data)
                state_space = dlplan.StateSpace(instance_data.state_space, state_pair_classifier.expanded_s_idxs, state_pair_classifier.generated_s_idxs)
                # Reinitialize instance_data
                instance_data.state_space.set_initial_state_index(old_initial_state_index)
                instance_data.state_space.set_goal_state_indices(old_goal_state_indices)
                instance_data.state_information = instance_data.state_space.compute_state_information()
                instance_data.goal_distance_information = instance_data.state_space.compute_goal_distance_information()
                # Construct subproblem_instance_data from acquired information
                subproblem_instance_data = InstanceData(
                    len(subproblem_instance_datas),
                    instance_data.instance_information,
                    instance_data.domain_data,
                    state_space,
                    state_space.compute_goal_distance_information(),
                    state_space.compute_state_information(),
                    None,
                    state_pair_classifier)
                subproblem_instance_data.tuple_graphs = TupleGraphFactory(width=0).make_tuple_graphs(subproblem_instance_data)
                # assert not subproblem_instance_data.goal_distance_information.get_deadend_state_indices()
                if not subproblem_instance_data.goal_distance_information.is_solvable() or \
                    subproblem_instance_data.goal_distance_information.is_trivially_solvable():
                    continue

                subproblem_instance_datas.append(subproblem_instance_data)
        if not subproblem_instance_datas:
            print(colored("Sketch rule does not induce any subproblems!", "red", "on_grey"))
            solution_policies.append(None)
            structurally_minimized_solution_policies.append(None)
            empirically_minimized_solution_policies.append(None)
            break
        subproblem_instance_datas = sorted(subproblem_instance_datas, key=lambda x : x.state_space.get_num_states())
        for instance_idx, instance_data in enumerate(subproblem_instance_datas):
            instance_data.id = instance_idx
            instance_data.state_space.get_instance_info().set_index(instance_idx)
        print("Number of subproblems:", len(subproblem_instance_datas))
        logging.info(colored(f"..done", "blue", "on_grey"))

        policy, structurally_minimized_policy, empirically_minimized_policy = learn_sketch(config, domain_data, subproblem_instance_datas, make_policy_asp_factory)
        solution_policies.append(policy)
        structurally_minimized_solution_policies.append(structurally_minimized_policy)
        empirically_minimized_solution_policies.append(empirically_minimized_policy)

    logging.info(colored("Summary:", "yellow", "on_grey"))
    print("Input sketch:")
    print(sketch.dlplan_policy.compute_repr())
    print("Learned policies by rule:")
    for rule in sketch.get_rules():
        print("Rule", rule.id, rule.dlplan_rule.compute_repr())
        if solution_policies[rule.id] is not None:
            print("Resulting policy:")
            solution_policies[rule.id].print()
        else:
            print("No policy found.")
    print()
    print("Learned structurally minimized policies by rule:")
    for rule in sketch.get_rules():
        print("Rule", rule.id, rule.dlplan_rule.compute_repr())
        if structurally_minimized_solution_policies[rule.id] is not None:
            print("Resulting structurally minimized sketch:")
            structurally_minimized_solution_policies[rule.id].print()
        else:
            print("No policy found.")
    print()
    print("Learned empirically minimized policies by rule:")
    for rule in sketch.get_rules():
        print("Rule", rule.id, rule.dlplan_rule.compute_repr())
        if empirically_minimized_solution_policies[rule.id] is not None:
            print("Resulting empirically minimized sketch:")
            empirically_minimized_solution_policies[rule.id].print()
        else:
            print("No policy found.")
    return ExitCode.Success, None


def make_policy_asp_factory(config):
    return PolicyASPFactory(config)
