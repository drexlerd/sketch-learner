import logging
import dlplan
import re
import subprocess
from typing import List
from dataclasses import dataclass
from enum import Enum
from collections import OrderedDict, defaultdict
from typing import Dict, MutableSet

from ..util.command import execute, read_file
from ..util.naming import filename_core
from .transition_system import TransitionSystemFactory, TransitionSystem
from .tuple_graph import TupleGraph, TupleGraphFactory, TupleGraphMinimizer
from .return_codes import ReturnCode
from ..domain_data.domain_data import DomainData


@dataclass
class InstanceData:
    """ """
    instance_filename: str
    domain_data: DomainData
    transition_system: TransitionSystem
    tuple_graphs_by_state_index: List[TupleGraph]
    minimized_tuple_graphs_by_state_index: List[TupleGraph]

    def print_statistics(self):
        self.transition_system.print_statistics()


class InstanceDataFactory:
    def make_instance_data(self, config, instance_information, domain_data):
        logging.info(f"Constructing InstanceData for filename {instance_information.name}")

        try:
            execute([config.sse_location / "fast-downward.py", domain_data.domain_filename, instance_information.instance_filename, "--translate-options", "--dump-static-atoms", "--dump-predicates", "--dump-goal-atoms", "--search-options", "--search", "dump_reachable_search_space()"], stdout=instance_information.state_space_filename, timeout=config.sse_time_limit, cwd=instance_information.workspace)
        except subprocess.TimeoutExpired:
            return None, ReturnCode.EXHAUSTED_TIME_LIMIT

        instance_info = dlplan.InstanceInfo(domain_data.vocabulary_info)
        dlplan_states, goals, forward_transitions = parse_state_space(instance_info, instance_information.workspace / "state_space.txt")
        parse_goal_atoms(instance_info, instance_information.workspace / "goal-atoms.txt")
        parse_static_atoms(instance_info, instance_information.workspace / "static-atoms.txt")
        if len(goals) == 0:
            return None, ReturnCode.UNSOLVABLE
        elif len(goals) == len(dlplan_states):
            return None, ReturnCode.TRIVIALLY_SOLVABLE
        elif len(dlplan_states) > config.max_states_per_instance:
            return None, ReturnCode.EXHAUSTED_SIZE_LIMIT

        transition_system = TransitionSystemFactory().parse_transition_system(dlplan_states, goals, forward_transitions)
        tuple_graphs_by_state_index, minimized_tuple_graphs_by_state_index = self._make_tuple_graphs(config, instance_info, transition_system)
        return InstanceData(instance_information.instance_filename, domain_data, transition_system, tuple_graphs_by_state_index, minimized_tuple_graphs_by_state_index), ReturnCode.SOLVABLE


    def _make_tuple_graphs(self,
        config,
        instance_info: dlplan.InstanceInfo,
        transition_system: TransitionSystem):
        tuple_graph_factory = TupleGraphFactory(
            config, instance_info, transition_system)
        tuple_graph_minimizer = TupleGraphMinimizer()
        tuple_graphs_by_state_index = [tuple_graph_factory.make_tuple_graph(config, i) for i in range(
            transition_system.get_num_states())]
        minimized_tuple_graphs_by_state_index = [tuple_graph_minimizer.minimize(tuple_graph) for tuple_graph in tuple_graphs_by_state_index]
        print("Tuple graph minimizer:")
        print(f"Num generated subgoal tuples: {tuple_graph_minimizer.num_generated}")
        print(f"Num pruned subgoal tuples: {tuple_graph_minimizer.num_pruned}")
        return tuple_graphs_by_state_index, minimized_tuple_graphs_by_state_index


def normalize_atom_name(name: str):
    tmp = name.replace('()', '').replace(')', '').replace('(', ',')
    if "=" in tmp:  # We have a functional atom
        tmp = tmp.replace("=", ',')
    return tmp.split(',')


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
    dlplan_states = list(dlplan_states.values())
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
