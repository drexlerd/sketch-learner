import logging
import dlplan
import re
import subprocess
from collections import OrderedDict, defaultdict
from typing import Dict, MutableSet

from ..util.command import execute, read_file

from .instance_data import InstanceData
from .subproblem import Subproblem
from .transition_system_factory import TransitionSystemFactory
from .return_codes import ReturnCode


class InstanceDataFactory:
    def make_instance_datas(self, config, domain_data):
        instance_datas = []
        for instance_information in config.instance_informations:
            instance_data, return_code = InstanceDataFactory().make_instance_data(config, len(instance_datas), instance_information, domain_data)
            if return_code == ReturnCode.SOLVABLE:
                assert instance_data is not None
                instance_data.print_statistics()
                instance_datas.append(instance_data)
            elif return_code == ReturnCode.TRIVIALLY_SOLVABLE:
                print(f"Instance is trivially solvable.")
            elif return_code == ReturnCode.UNSOLVABLE:
                print(f"Instance is unsolvable.")
            elif return_code == ReturnCode.EXHAUSTED_SIZE_LIMIT:
                print(f"Instance is too large. Maximum number of allowed states is: {config.max_states_per_instance}.")
            elif return_code == ReturnCode.EXHAUSTED_TIME_LIMIT:
                print(f"Instance is too large. Time limit is: {config.sse_time_limit}")
        instance_datas = sorted(instance_datas, key=lambda x : x.transition_system.get_num_states())
        return instance_datas

    def make_instance_data(self, config, instance_idx, instance_information, domain_data):
        try:
            execute([config.sse_location / "fast-downward.py", domain_data.domain_filename, instance_information.instance_filename, "--translate-options", "--dump-static-atoms", "--dump-predicates", "--dump-goal-atoms", "--search-options", "--search", "dump_reachable_search_space()"], stdout=instance_information.state_space_filename, timeout=config.sse_time_limit, cwd=instance_information.workspace)
        except subprocess.TimeoutExpired:
            return None, ReturnCode.EXHAUSTED_TIME_LIMIT

        instance_info = dlplan.InstanceInfo(domain_data.vocabulary_info)
        s_idx_to_dlplan_state, goals, forward_transitions = parse_state_space(instance_info, instance_information.workspace / "state_space.txt")
        parse_goal_atoms(instance_info, instance_information.workspace / "goal-atoms.txt")
        parse_static_atoms(instance_info, instance_information.workspace / "static-atoms.txt")
        if len(goals) == 0:
            return None, ReturnCode.UNSOLVABLE
        elif len(goals) == len(s_idx_to_dlplan_state):
            return None, ReturnCode.TRIVIALLY_SOLVABLE
        elif len(s_idx_to_dlplan_state) > config.max_states_per_instance:
            return None, ReturnCode.EXHAUSTED_SIZE_LIMIT

        transition_system = TransitionSystemFactory().parse_transition_system(s_idx_to_dlplan_state, goals, forward_transitions)
        return InstanceData(instance_idx, instance_information, domain_data, transition_system, instance_info), ReturnCode.SOLVABLE

    def make_instance_data_from_subproblem(self, subproblem: Subproblem):
        """
        Copies the subproblems InstanceData and then adds seed predicates
        and static seed atoms for the initial state.
        """
        # Get a copy of the InstanceData
        instance_data = self.reparse_instance_data(subproblem.instance_data)
        # Create a transition system that reflects the subproblem
        transition_system = TransitionSystemFactory().restrict_transition_system_by_subproblem(instance_data.transition_system, subproblem)
        instance_data.transition_system = transition_system
        # Add static seed atoms for initial state
        for atom_idx in instance_data.transition_system.s_idx_to_dlplan_state[subproblem.root_idx].get_atom_idxs():
            atom = instance_data.instance_info.get_atom(atom_idx)
            instance_data.instance_info.add_static_atom(atom.get_predicate().get_name() + "_r", [object.get_name() for object in atom.get_objects()])
        return instance_data

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
        transition_system = TransitionSystemFactory().parse_transition_system(dlplan_states, goals, forward_transitions)
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
    dlplan_state = dlplan.State(instance_info, dlplan_atoms)
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
