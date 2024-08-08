from typing import List, Dict, MutableSet
from collections import defaultdict

from .tuple_graph_equivalence import TupleGraphEquivalence
from .iteration_data import IterationData

from ..preprocessing import PreprocessingData


def compute_tuple_graph_equivalences(preprocessing_data: PreprocessingData,
                                     iteration_data: IterationData) -> None:
    """ Computes information for all subgoal states, tuples and rules over F.
    """
    num_nodes = 0

    instance_idx_to_ss_idx_to_tuple_graph_equivalence: Dict[int, Dict[int, TupleGraphEquivalence]] = dict()

    for instance_data in iteration_data.instance_datas:
        tuple_graph_equivalence_per_instance: Dict[int, TupleGraphEquivalence] = dict()

        for mimir_ss_state_idx in range(instance_data.mimir_ss.get_num_states()):
            if instance_data.mimir_ss.is_deadend_state(mimir_ss_state_idx):
                continue

            tuple_graph = preprocessing_data.ss_state_idx_to_tuple_graph[instance_data.idx][mimir_ss_state_idx]
            tuple_graph_vertices_by_distance = tuple_graph.get_vertices_grouped_by_distance()
            tuple_graph_states_by_distance = tuple_graph.get_states_grouped_by_distance()

            t_idx_to_r_idxs: Dict[int, MutableSet[int]] = dict()
            t_idx_to_distance: Dict[int, int] = dict()
            r_idx_to_deadend_distance: Dict[int, int] = dict()

            for s_distance, mimir_ss_states_prime in enumerate(tuple_graph_states_by_distance):
                for mimir_ss_state_prime in mimir_ss_states_prime:
                    mimir_ss_state_prime_idx = instance_data.mimir_ss.get_state_index(mimir_ss_state_prime)

                    r_idx = iteration_data.instance_idx_to_ss_idx_to_state_pair_equivalence[instance_data.idx][mimir_ss_state_idx].subgoal_gfa_state_id_to_r_idx[mimir_ss_state_prime_idx]

                    if instance_data.mimir_ss.is_deadend_state(mimir_ss_state_prime_idx):
                        r_idx_to_deadend_distance[r_idx] = min(r_idx_to_deadend_distance.get(r_idx, float("inf")), s_distance)

            for s_distance, tuple_vertex_group in enumerate(tuple_graph_vertices_by_distance):
                for tuple_vertex in tuple_vertex_group:
                    t_idx = tuple_vertex.get_index()
                    r_idxs = set()
                    for mimir_ss_state_prime in tuple_vertex.get_states():
                        mimir_ss_state_prime_idx = instance_data.mimir_ss.get_state_index(mimir_ss_state_prime)

                        r_idx = iteration_data.instance_idx_to_ss_idx_to_state_pair_equivalence[instance_data.idx][mimir_ss_state_idx].subgoal_gfa_state_id_to_r_idx[mimir_ss_state_prime_idx]
                        r_idxs.add(r_idx)
                    t_idx_to_distance[t_idx] = s_distance
                    t_idx_to_r_idxs[t_idx] = r_idxs
                    num_nodes += 1

            tuple_graph_equivalence_per_instance[mimir_ss_state_idx] = TupleGraphEquivalence(t_idx_to_r_idxs, t_idx_to_distance, r_idx_to_deadend_distance)

        instance_idx_to_ss_idx_to_tuple_graph_equivalence[instance_data.idx] = tuple_graph_equivalence_per_instance

    print("Tuple graph equivalence construction statistics:")
    print("Num nodes:", num_nodes)

    return instance_idx_to_ss_idx_to_tuple_graph_equivalence


def minimize_tuple_graph_equivalences(preprocessing_data: PreprocessingData,
                                      iteration_data: IterationData):
    num_kept_nodes = 0
    num_orig_nodes = 0

    for instance_data in iteration_data.instance_datas:
        for mimir_ss_state_idx in range(instance_data.mimir_ss.get_num_states()):
            if instance_data.mimir_ss.is_deadend_state(mimir_ss_state_idx):
                continue

            tuple_graph = preprocessing_data.ss_state_idx_to_tuple_graph[instance_data.idx][mimir_ss_state_idx]
            tuple_graph_equivalence = iteration_data.instance_idx_to_ss_idx_to_tuple_graph_equivalence[instance_data.idx][mimir_ss_state_idx]
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
            for tuple_vertex_group in tuple_graph.get_vertices_grouped_by_distance():
                for tuple_vertex in tuple_vertex_group:
                    t_idx = tuple_vertex.get_index()
                    r_idxs = frozenset(tuple_graph_equivalence.t_idx_to_r_idxs[t_idx])
                    if order.get(t_idx, 0) != 0:
                        continue
                    if r_idxs in representative_r_idxs:
                        continue
                    representative_r_idxs.add(r_idxs)
                    # found tuple with minimal number of rules
                    selected_t_idxs.add(t_idx)

            # restrict to selected tuples
            t_idx_to_r_idxs: Dict[int, MutableSet[int]] = dict()
            t_idx_to_distance: Dict[int, int] = dict()
            for t_idx, r_idxs in tuple_graph_equivalence.t_idx_to_r_idxs.items():
                if t_idx in selected_t_idxs:
                    t_idx_to_r_idxs[t_idx] = r_idxs
                    num_kept_nodes += 1
                num_orig_nodes += 1
            for t_idx, distance in tuple_graph_equivalence.t_idx_to_distance.items():
                if t_idx in selected_t_idxs:
                    t_idx_to_distance[t_idx] = distance

            iteration_data.instance_idx_to_ss_idx_to_tuple_graph_equivalence[instance_data.idx][mimir_ss_state_idx] = TupleGraphEquivalence(t_idx_to_r_idxs, t_idx_to_distance, tuple_graph_equivalence.r_idx_to_deadend_distance)

    print("Tuple graph equivalence minimization statistics:")
    print("Num orig nodes:", num_orig_nodes)
    print("Num kept nodes:", num_kept_nodes)
