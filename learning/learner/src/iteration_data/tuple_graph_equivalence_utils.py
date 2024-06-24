from typing import List, Dict, MutableSet
from collections import defaultdict

from .tuple_graph_equivalence import TupleGraphEquivalence

from ..domain_data.domain_data import DomainData
from ..instance_data.instance_data import InstanceData, StateFinder


def compute_tuple_graph_equivalences(domain_data: DomainData,
    instance_datas: List[InstanceData],
    selected_instance_datas: List[InstanceData],
    state_finder: StateFinder) -> None:
    """ Computes information for all subgoal states, tuples and rules over F.
    """
    num_nodes = 0

    gfa_state_id_to_tuple_graph_equivalence: Dict[int, TupleGraphEquivalence] = dict()

    for gfa_state in domain_data.gfa_states:
        instance_idx = gfa_state.get_abstraction_id()
        instance_data = instance_datas[instance_idx]
        gfa_state_id = gfa_state.get_id()
        gfa_state_idx = instance_data.gfa.get_state_index(gfa_state)
        if instance_data.gfa.is_deadend_state(gfa_state_idx):
            continue

        tuple_graph = domain_data.gfa_state_id_to_tuple_graph[gfa_state_id]

        t_idx_to_r_idxs: Dict[int, MutableSet[int]] = dict()
        t_idx_to_distance: Dict[int, int] = dict()
        r_idx_to_deadend_distance: Dict[int, int] = dict()

        for s_distance, mimir_ss_states_prime in enumerate(tuple_graph.get_states_by_distance()):
            for mimir_ss_state_prime in mimir_ss_states_prime:
                gfa_state_prime = state_finder.get_gfa_state_from_ss_state_idx(instance_idx, instance_data.mimir_ss.get_state_index(mimir_ss_state_prime))
                gfa_state_prime_id = gfa_state_prime.get_id()
                instance_prime_idx = gfa_state_prime.get_abstraction_id()
                instance_data_prime = instance_datas[instance_prime_idx]
                gfa_state_prime_idx = instance_data_prime.gfa.get_state_index(gfa_state_prime)

                r_idx = domain_data.gfa_state_id_to_state_pair_equivalence[gfa_state_id].subgoal_gfa_state_id_to_r_idx[gfa_state_prime_id]

                if instance_data_prime.gfa.is_deadend_state(gfa_state_prime_idx):
                    r_idx_to_deadend_distance[r_idx] = min(r_idx_to_deadend_distance.get(r_idx, float("inf")), s_distance)

        for s_distance, tuple_vertex_idxs in enumerate(tuple_graph.get_vertex_indices_by_distances()):
            for tuple_vertex_idx in tuple_vertex_idxs:
                tuple_vertex = tuple_graph.get_vertices()[tuple_vertex_idx]
                t_idx = tuple_vertex.get_identifier()
                r_idxs = set()
                for mimir_ss_state_prime in tuple_vertex.get_states():
                    gfa_state_prime = state_finder.get_gfa_state_from_ss_state_idx(instance_idx, instance_data.mimir_ss.get_state_index(mimir_ss_state_prime))
                    gfa_state_prime_id = gfa_state_prime.get_id()
                    r_idx = domain_data.gfa_state_id_to_state_pair_equivalence[gfa_state_id].subgoal_gfa_state_id_to_r_idx[gfa_state_prime_id]
                    r_idxs.add(r_idx)
                t_idx_to_distance[t_idx] = s_distance
                t_idx_to_r_idxs[t_idx] = r_idxs
                num_nodes += 1

        gfa_state_id_to_tuple_graph_equivalence[gfa_state_id] = TupleGraphEquivalence(t_idx_to_r_idxs, t_idx_to_distance, r_idx_to_deadend_distance)
    domain_data.gfa_state_id_to_tuple_graph_equivalence = gfa_state_id_to_tuple_graph_equivalence

    print("Tuple graph equivalence construction statistics:")
    print("Num nodes:", num_nodes)


def minimize_tuple_graph_equivalences(instance_datas: List[InstanceData]):
    num_kept_nodes = 0
    num_orig_nodes = 0
    for instance_data in instance_datas:
        for root_idx, tuple_graph in instance_data.per_state_tuple_graphs.gfa_state_idx_to_tuple_graph.items():
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
            for tuple_vertex_indices in tuple_graph.get_vertex_indices_by_distances():
                for tuple_vertex_index in tuple_vertex_indices:
                    tuple_vertex = tuple_graph.get_vertices()[tuple_vertex_index]
                    t_idx = tuple_vertex.get_identifier()
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
