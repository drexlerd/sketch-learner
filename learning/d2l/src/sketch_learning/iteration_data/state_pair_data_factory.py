from typing import List

from .state_pair_data import StatePair, StatePairData

from ..instance_data.tuple_graph_data import TupleGraphData
from ..instance_data.subproblem import SubproblemData


class StatePairDataFactory:
    def make_state_pairs_from_tuple_graphs(self, tuple_graph_datas: List[TupleGraphData]):
        state_pair_datas = []
        states = set()
        for tuple_graph_data in tuple_graph_datas:
            state_pairs = []
            for tuple_graph in tuple_graph_data.tuple_graphs_by_state_index:
                if tuple_graph is None: continue
                for target_idxs in tuple_graph.s_idxs_by_distance:
                    for target_idx in target_idxs:
                        state_pairs.append(StatePair(tuple_graph.root_idx, target_idx))
                        states.add(tuple_graph.root_idx)
                        states.add(target_idx)
            state_pair_datas.append(StatePairData(state_pairs, list(states)))
        return state_pair_datas

    def make_state_pairs_from_subproblem_data(self, subproblem_data: SubproblemData):
        state_pairs = set()
        for _, transitions in subproblem_data.forward_transitions.items():
            for transition in transitions:
                state_pairs.add(StatePair(transition.source_idx, transition.target_idx))
        return StatePairData(subproblem_data, list(state_pairs))
