import logging
import copy
import dlplan
import math
import re
import subprocess
from collections import OrderedDict, defaultdict
from typing import Dict, MutableSet

from sketch_learning.iteration_data.sketch import SketchRule

from ..util.command import read_file

from .instance_data import InstanceData


class InstanceDataFactory:
    def make_instance_datas(self, config, domain_data):
        instance_datas = []
        for instance_information in config.instance_informations:
            logging.info(f"Constructing InstanceData for filename {instance_information.instance_filename}")
            exitcode = dlplan.StateSpaceGenerator().generate_state_space(str(domain_data.domain_filename), str(instance_information.instance_filename))
            state_space = dlplan.StateSpaceReader().read(domain_data.vocabulary_info)
            goal_distance_information = state_space.compute_goal_distance_information()
            if not goal_distance_information.is_solvable() or \
                goal_distance_information.is_trivially_solvable():
                continue
            elif goal_distance_information.is_solvable():
                state_information = state_space.compute_state_information()
                instance_datas.append(InstanceData(len(instance_datas), instance_information, domain_data, state_space, goal_distance_information, state_information))
        # Sort the instances according to size and fix the indices afterwards
        instance_datas = sorted(instance_datas, key=lambda x : x.state_space.get_num_states())
        for instance_idx, instance_data in enumerate(instance_datas):
            instance_data.id = instance_idx
        return instance_datas

    def make_subproblem_instance_data(self, subproblem_idx: int, instance_data: InstanceData, root_idx: int, rule: SketchRule):
        state_space_copy = copy.deepcopy(instance_data.state_space)
        state_space_copy.set_initial_state_index(root_idx)
        # Add static seed atoms for initial state
        # for atom_idx in instance_data.transition_system.s_idx_to_dlplan_state[root_idx].get_atom_idxs():
        #    atom = instance_data.instance_info.get_atom(atom_idx)
        #    instance_data.instance_info.add_static_atom(atom.get_predicate().get_name() + "_r", [object.get_name() for object in atom.get_objects()])
        return InstanceData(subproblem_idx, instance_data.instance_information, instance_data.domain_data, state_space_copy)

    def _compute_closest_subgoal_states(self, instance_data: InstanceData, root_idx: int, rule: SketchRule):
        evaluation_cache = dlplan.EvaluationCache(len(rule.sketch.dlplan_policy.get_boolean_features()), len(rule.sketch.dlplan_policy.get_numerical_features()))
        source_state = instance_data.transition_system.s_idx_to_dlplan_state[root_idx]
        if not rule.dlplan_rule.evaluate_conditions(source_state, evaluation_cache):
            return set()
        layers, _ = instance_data.transition_system.partition_states_by_distance(states=[root_idx], forward=True, stop_upon_goal=False)
        for layer in layers:
            closest_subgoal_states = set()
            for target_idx in layer:
                target_state = instance_data.transition_system.s_idx_to_dlplan_state[target_idx]
                if rule.dlplan_rule.evaluate_effects(source_state, target_state, evaluation_cache):
                    closest_subgoal_states.add(target_idx)
            if closest_subgoal_states:
                return closest_subgoal_states
        return set()

    def reparse_instance_data(self, instance_data: InstanceData):
        """
        This function allows to reparse an existing state space
        and construct objects from it that are independent of other InstanceData.

        This is useful in cases where we need a new dlplan InstanceInfo
        because we want to add seed predicates and seed static atoms.
        """
        instance_idx = instance_data.id
        instance_information = instance_data.instance_information
        domain_data = instance_data.domain_data

        instance_info = dlplan.InstanceInfo(domain_data.vocabulary_info)
        dlplan_states, goals, forward_transitions = parse_state_space(instance_info, instance_information.workspace / "state_space.txt")
        parse_goal_atoms(instance_info, instance_information.workspace / "goal-atoms.txt")
        parse_static_atoms(instance_info, instance_information.workspace / "static-atoms.txt")
        transition_system = TransitionSystemFactory().make_transition_system(dlplan_states, goals, forward_transitions)
        return InstanceData(instance_idx, instance_information, domain_data, transition_system, instance_info)


def normalize_atom_name(name: str):
    tmp = name.replace('()', '').replace(')', '').replace('(', ',')
    if "=" in tmp:  # We have a functional atom
        tmp = tmp.replace("=", ',')
    return [x.strip() for x in tmp.split(',')]


def parse_static_atoms(instance_info: dlplan.InstanceInfo, filename: str):
    for line in read_file(filename):
        normalized_atom = normalize_atom_name(line)
        instance_info.add_static_atom(normalized_atom[0], normalized_atom[1:])


def parse_goal_atoms(instance_info: dlplan.InstanceInfo, filename: str):
    for line in read_file(filename):
        normalized_atom = normalize_atom_name(line)
        instance_info.add_static_atom(normalized_atom[0] + "_g", normalized_atom[1:])


def parse_state_space(instance_info: dlplan.InstanceInfo, filename: str):
    atom_idx_to_dlplan_atom = dict()
    dlplan_states = OrderedDict()
    goals = set()
    forward_transitions = defaultdict(set)
    for line in read_file(filename):
        if line.startswith("F "):
            parse_fact_line(instance_info, line, atom_idx_to_dlplan_atom)
        elif line.startswith("G "):
            parse_state_line(instance_info, line, atom_idx_to_dlplan_atom, dlplan_states, goals)
        elif line.startswith("N "):
            parse_state_line(instance_info, line, atom_idx_to_dlplan_atom, dlplan_states, goals)
        elif line.startswith("T "):
            parse_transition_line(line, forward_transitions)
    return dlplan_states, goals, forward_transitions


def parse_fact_line(instance_info: dlplan.InstanceInfo, line: str, atom_idx_to_dlplan_atom: Dict[int, dlplan.Atom]):
    """
    E.g.
    at-robby(roomb)
    at(ball1, rooma)
    """
    result = re.findall(r"F (\d+) (.*)", line)
    assert len(result) == 1 and len(result[0]) == 2
    atom_idx = int(result[0][0])
    atom_name = result[0][1]
    normalized_atom = normalize_atom_name(atom_name)
    if normalized_atom[0].startswith("dummy"):
        return
    elif normalized_atom[0].startswith("new-axiom@"):
        return
    dlplan_atom = instance_info.add_atom(normalized_atom[0], normalized_atom[1:])
    atom_idx_to_dlplan_atom[atom_idx] = dlplan_atom


def parse_state_line(instance_info: dlplan.InstanceInfo, line: str, atom_idx_to_dlplan_atom: Dict[int, dlplan.Atom], states: Dict[int, dlplan.State], goals: MutableSet[int]):
    """
    E.g.
    N 127 0 2 8 10 12 17 18
    G 129 0 2 8 10 11 17 19
    """
    result = re.findall(r"[NG] (.*)", line)
    assert len(result) == 1
    indices = [int(x) for x in result[0].split(" ")]
    state_idx = indices[0]
    atom_idxs = indices[1:]
    dlplan_atoms = [atom_idx_to_dlplan_atom[atom_idx] for atom_idx in atom_idxs if atom_idx in atom_idx_to_dlplan_atom]
    dlplan_state = dlplan.State(instance_info, dlplan_atoms, state_idx)
    states[state_idx] = dlplan_state
    if line.startswith("G "):
        goals.add(state_idx)


def parse_transition_line(line: str, forward_transitions: Dict[int, MutableSet[int]]):
    """
    E.g.
    T 0 5
    T 1 4
    """
    result = re.findall(r"T (.*) (.*)", line)
    assert len(result) == 1
    source_idx = int(result[0][0])
    target_idx = int(result[0][1])
    forward_transitions[source_idx].add(target_idx)
