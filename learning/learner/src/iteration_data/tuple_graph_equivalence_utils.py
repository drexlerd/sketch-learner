import math
from typing import List
from collections import defaultdict

from .tuple_graph_equivalence import TupleGraphEquivalence, PerStateTupleGraphEquivalences

from ..instance_data.instance_data import InstanceData


def compute_tuple_graph_equivalences(instance_datas: List[InstanceData]) -> None:
    """ Computes information for all subgoal states, tuples and rules over F.
    """
    num_nodes = 0
    for instance_data in instance_datas:
        per_state_tuple_graph_equivalences = PerStateTupleGraphEquivalences()
        for s_idx, tuple_graph in instance_data.per_state_tuple_graphs.s_idx_to_tuple_graph.items():
            if instance_data.is_deadend(s_idx):
                continue
            state_pair_equivalence = instance_data.per_state_state_pair_equivalences.s_idx_to_state_pair_equivalence[s_idx]
            tuple_graph_equivalence = TupleGraphEquivalence()
            # rule distances, deadend rule distances
            for state_distance, s_prime_idxs in enumerate(tuple_graph.get_state_indices_by_distance()):
                for s_prime_idx in set(instance_data.state_index_to_representative_state_index[s] for s in s_prime_idxs):
                    r_idx = state_pair_equivalence.subgoal_state_to_r_idx[s_prime_idx]
                    if instance_data.is_deadend(s_prime_idx):
                        tuple_graph_equivalence.r_idx_to_deadend_distance[r_idx] = min(tuple_graph_equivalence.r_idx_to_deadend_distance.get(r_idx, math.inf), state_distance)
            for subgoal_distance, tuple_node_indices in enumerate(tuple_graph.get_tuple_node_indices_by_distance()):
                for tuple_node_index in tuple_node_indices:
                    tuple_node = tuple_graph.get_tuple_nodes()[tuple_node_index]
                    t_idx = tuple_node.get_index()
                    r_idxs = set()
                    for s_prime_idx in set(instance_data.state_index_to_representative_state_index[s] for s in tuple_node.get_state_indices()):
                        r_idx = state_pair_equivalence.subgoal_state_to_r_idx[s_prime_idx]
                        r_idxs.add(r_idx)
                    tuple_graph_equivalence.t_idx_to_distance[t_idx] = subgoal_distance
                    tuple_graph_equivalence.t_idx_to_r_idxs[t_idx] = r_idxs
                    num_nodes += 1
            per_state_tuple_graph_equivalences.s_idx_to_tuple_graph_equivalence[s_idx] = tuple_graph_equivalence
        instance_data.per_state_tuple_graph_equivalences = per_state_tuple_graph_equivalences

    print("Tuple graph equivalence construction statistics:")
    print("Num nodes:", num_nodes)




def minimize_tuple_graph_equivalences(instance_datas: List[InstanceData]):
    num_kept_nodes = 0
    num_orig_nodes = 0
    for instance_data in instance_datas:
        for root_idx, tuple_graph in instance_data.per_state_tuple_graphs.s_idx_to_tuple_graph.items():
            if instance_data.is_deadend(root_idx):
                continue

            tuple_graph_equivalence = instance_data.per_state_tuple_graph_equivalences.s_idx_to_tuple_graph_equivalence[root_idx]
            # compute order
            order = defaultdict(set)
            for t_idx_1 in tuple_graph_equivalence.t_idx_to_r_idxs.keys():
                r_idxs_1 = frozenset(tuple_graph_equivalence.t_idx_to_r_idxs[t_idx_1])
                for t_idx_2 in tuple_graph_equivalence.t_idx_to_r_idxs.keys():
                    if t_idx_1 == t_idx_2:
                        continue
                    r_idxs_2 = frozenset(tuple_graph_equivalence.t_idx_to_r_idxs[t_idx_2])
                    if r_idxs_1.issubset(r_idxs_2) and r_idxs_1 != r_idxs_2:
                        # t_2 gets dominated by t_1
                        order[t_idx_2].add(t_idx_1)
            # select tuple nodes according to order
            selected_t_idxs = set()
            representative_r_idxs = set()
            for tuple_node_indices in tuple_graph.get_tuple_node_indices_by_distance():
                for tuple_node_index in tuple_node_indices:
                    tuple_node = tuple_graph.get_tuple_nodes()[tuple_node_index]
                    t_idx = tuple_node.get_index()
                    r_idxs = frozenset(tuple_graph_equivalence.t_idx_to_r_idxs[t_idx])
                    if order.get(t_idx, 0) != 0:
                        continue
                    if r_idxs in representative_r_idxs:
                        continue
                    representative_r_idxs.add(r_idxs)
                    # found tuple with minimal number of rules
                    selected_t_idxs.add(t_idx)

            # restrict to selected tuples
            t_idx_to_r_idxs = defaultdict(set)
            t_idx_to_distance = dict()
            for t_idx, r_idxs in tuple_graph_equivalence.t_idx_to_r_idxs.items():
                if t_idx in selected_t_idxs:
                    t_idx_to_r_idxs[t_idx] = r_idxs
                    num_kept_nodes += 1
                num_orig_nodes += 1
            for t_idx, distance in tuple_graph_equivalence.t_idx_to_distance.items():
                if t_idx in selected_t_idxs:
                    t_idx_to_distance[t_idx] = distance
            tuple_graph_equivalence.t_idx_to_r_idxs = t_idx_to_r_idxs
            tuple_graph_equivalence.t_idx_to_distance = t_idx_to_distance

    print("Tuple graph equivalence minimization statistics:")
    print("Num orig nodes:", num_orig_nodes)
    print("Num kept nodes:", num_kept_nodes)
