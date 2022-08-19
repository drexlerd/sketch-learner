import math
from typing import List
from collections import defaultdict

from .state_pair_equivalence_data import StatePairEquivalenceData
from .tuple_graph_equivalence_data import TupleGraphEquivalenceData

from ..instance_data.instance_data import InstanceData
from ..instance_data.tuple_graph_data import TupleGraphData


class TupleGraphEquivalenceDataFactory:
    def make_equivalence_data(self, instance_datas: List[InstanceData], tuple_graph_datas: List[TupleGraphData], state_pair_equivalence_datas: List[StatePairEquivalenceData]):
        tuple_graph_equivalence_datas = []
        for instance_data, tuple_graph_data, state_pair_equivalence_data in zip(instance_datas, tuple_graph_datas, state_pair_equivalence_datas):
            tuple_graph_equivalence_data = []
            for tuple_graph in tuple_graph_data.tuple_graphs_by_state_index:
                if tuple_graph is None:
                    tuple_graph_equivalence_data.append(None)
                    continue
                # rule distances, deadend rule distances
                r_idxs_by_distance = []
                r_idx_to_deadend_distance = dict()
                r_idx_to_distance = dict()
                for d, layer in enumerate(tuple_graph.s_idxs_by_distance):
                    r_idxs = set()
                    for s_idx in layer:
                        r_idx = state_pair_equivalence_data.state_pair_to_r_idx[(tuple_graph.root_idx, s_idx)]
                        r_idxs.add(r_idx)
                        if instance_data.transition_system.is_deadend(s_idx):
                            # the first time we write r_idx = d, d is smallest value.
                            r_idx_to_deadend_distance[r_idx] = min(r_idx_to_deadend_distance.get(r_idx, math.inf), d)
                        r_idx_to_distance[r_idx] = min(r_idx_to_distance.get(r_idx, math.inf), d)
                    r_idxs_by_distance.append(r_idxs)
                # map tuple to rules and vice versa
                t_idx_to_r_idxs = defaultdict(set)
                r_idx_to_t_idxs = defaultdict(set)
                for t_idxs in tuple_graph.t_idxs_by_distance:
                    for t_idx in t_idxs:
                        for s_idx in tuple_graph.t_idx_to_s_idxs[t_idx]:
                            r_idx = state_pair_equivalence_data.state_pair_to_r_idx[(tuple_graph.root_idx, s_idx)]
                            t_idx_to_r_idxs[t_idx].add(r_idx)
                            r_idx_to_t_idxs[r_idx].add(t_idx)
                tuple_graph_equivalence_data.append(TupleGraphEquivalenceData(r_idxs_by_distance, t_idx_to_r_idxs, r_idx_to_t_idxs, r_idx_to_deadend_distance, r_idx_to_distance))
            tuple_graph_equivalence_datas.append(tuple_graph_equivalence_data)
        return tuple_graph_equivalence_datas
