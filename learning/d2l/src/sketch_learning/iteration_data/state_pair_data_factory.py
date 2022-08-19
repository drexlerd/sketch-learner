from typing import List

from .state_pair_data import StatePair, StatePairData

from ..instance_data.tuple_graph_data import TupleGraphData
from ..instance_data.subproblem import SubproblemData


class StatePairDataFactory:
    def make_state_pairs_from_tuple_graph_data(self, tuple_graph_data: TupleGraphData):
        state_pairs = []
        for tuple_graph in tuple_graph_data.tuple_graphs_by_state_index:
            if tuple_graph is None: continue
            for target_idxs in tuple_graph.s_idxs_by_distance:
                for target_idx in target_idxs:
                    state_pairs.append(StatePair(tuple_graph.root_idx, target_idx))
        return StatePairData(state_pairs)

    def make_state_pairs_from_subproblem_data(self, subproblem_data: SubproblemData):
        state_pairs = []
        for _, transitions in subproblem_data.forward_transitions.items():
            for transition in transitions:
                state_pairs.append(StatePair(transition.source_idx, transition.target_idx))
        return StatePairData(state_pairs)
