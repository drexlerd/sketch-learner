import math
from typing import List
from collections import defaultdict

from .tuple_graph_equivalence import TupleGraphEquivalence

from ..instance_data.instance_data import InstanceData
from ..instance_data.state_pair import StatePair


class TupleGraphEquivalenceFactory:
    def make_tuple_graph_equivalence_datas(self, instance_data: InstanceData):
        tuple_graph_equivalences = dict()
        for root_idx, tuple_graph in instance_data.tuple_graphs.items():
            if not instance_data.goal_distance_information.is_alive(root_idx):
                continue
            # rule distances, deadend rule distances
            r_idx_to_deadend_distance = dict()
            r_idx_to_distance = dict()
            for distance, layer in enumerate(tuple_graph.get_state_indices_by_distance()):
                r_idxs = set()
                for s_idx in layer:
                    r_idx = instance_data.state_pair_equivalence.state_pair_to_r_idx[StatePair(tuple_graph.get_root_state_index(), s_idx)]
                    r_idxs.add(r_idx)
                    if instance_data.goal_distance_information.is_deadend(s_idx):
                        # the first time we write r_idx = d, d is smallest value.
                        r_idx_to_deadend_distance[r_idx] = min(r_idx_to_deadend_distance.get(r_idx, math.inf), distance)
                    r_idx_to_distance[r_idx] = min(r_idx_to_distance.get(r_idx, math.inf), distance)
            # map tuple to rules and vice versa
            t_idx_to_r_idxs = defaultdict(set)
            t_idx_to_distance = dict()
            for distance, tuple_nodes in enumerate(tuple_graph.get_tuple_nodes_by_distance()):
                for tuple_node in tuple_nodes:
                    t_idx = tuple_node.get_tuple_index()
                    t_idx_to_distance[t_idx] = distance
                    for s_idx in tuple_node.get_state_indices():
                        r_idx = instance_data.state_pair_equivalence.state_pair_to_r_idx[StatePair(tuple_graph.get_root_state_index(), s_idx)]
                        t_idx_to_r_idxs[t_idx].add(r_idx)
            tuple_graph_equivalences[root_idx] = TupleGraphEquivalence(t_idx_to_r_idxs, t_idx_to_distance, r_idx_to_deadend_distance, r_idx_to_distance)
        return tuple_graph_equivalences
