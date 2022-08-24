from dataclasses import dataclass
from re import T
from typing import List

from .state_pair import StatePair

from ..instance_data.tuple_graph import TupleGraph
from ..instance_data.subproblem import Subproblem

@dataclass
class StatePairFactoryStatistics:
    num_state_pairs: int = 0

    def increment_num_state_pairs(self):
        self.num_state_pairs += 1

    def print(self):
        print("Number of state pairs:", self.num_state_pairs)


class StatePairFactory:
    def __init__(self):
        self.statistics = StatePairFactoryStatistics()

    def make_state_pairs_from_tuple_graphs(self, tuple_graphs: List[TupleGraph]):
        state_pairs = []
        for tuple_graph in tuple_graphs:
            if tuple_graph is None: continue
            for distance, target_idxs in enumerate(tuple_graph.s_idxs_by_distance):
                for target_idx in target_idxs:
                    state_pairs.append(StatePair(tuple_graph.root_idx, target_idx, distance))
                    self.statistics.increment_num_state_pairs()
        return state_pairs

    def make_state_pairs_from_subproblem(self, subproblems: Subproblem):
        state_pairs = []
        for _, transitions in subproblems.forward_transitions.items():
            for transition in transitions:
                state_pairs.append(StatePair(transition.source_idx, transition.target_idx, 1))
                self.statistics.increment_num_state_pairs()
        return state_pairs
