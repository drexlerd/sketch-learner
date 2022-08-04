import dlplan
import math
from typing import Dict, List, MutableSet, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

from ..instance_data.instance_data import InstanceData
from ..instance_data.general_subproblem import GeneralSubproblemData


@dataclass
class StatePair:
    source_idx: int
    target_idx: int

    def __eq__(self, other):
        return self.source_idx == other.source_idx and self.target_idx == other.target_idx

    def __hash__(self):
        return hash((self.source_idx, self.target_idx))


@dataclass
class StatePairData:
    """
    StatePairData contains:
        (1) all state pairs for that can be pi-compatible, and
        (2) all states that are part of a state pair in (1)


    This allows a common interface for computing sketches or policies.
    The reason is that we do not care about the transition labels
    and just the state pair.
    """
    state_pairs: List[StatePair]
    states: List[int]


class StatePairDataFactory:
    def make_state_pairs_from_tuple_graphs(self, instance_datas: List[InstanceData]):
        state_pair_datas = []
        states = set()
        for instance_data in instance_datas:
            state_pairs = []
            for tuple_graph in instance_data.tuple_graphs_by_state_index:
                if tuple_graph is None: continue
                for target_idxs in tuple_graph.s_idxs_by_distance:
                    for target_idx in target_idxs:
                        state_pairs.append(StatePair(tuple_graph.root_idx, target_idx))
                        states.add(tuple_graph.root_idx)
                        states.add(target_idx)
            state_pair_datas.append(StatePairData(state_pairs, list(states)))
        return state_pair_datas

    def make_state_pairs_from_general_subproblem_datas(self, general_subproblem_datas: List[GeneralSubproblemData]):
        state_pair_datas = []
        states = set()
        for general_subproblem_data in general_subproblem_datas:
            state_pairs = set()
            for _, transitionss in general_subproblem_data.forward_transitions.items():
                for transitions in transitionss:
                    for transition in transitions:
                        state_pairs.add(StatePair(transition.source_idx, transition.target_idx))
                        states.add(transition.source_idx)
                        states.add(transition.target_idx)
            state_pair_datas.append(StatePairData(list(state_pairs), list(states)))
        return state_pair_datas
