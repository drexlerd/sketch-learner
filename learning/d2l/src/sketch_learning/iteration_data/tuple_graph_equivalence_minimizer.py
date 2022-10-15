import dlplan
import math

from collections import defaultdict
from typing import Dict, List, MutableSet, Tuple
from dataclasses import dataclass

from .tuple_graph_equivalence import TupleGraphEquivalence
from ..instance_data.instance_data import InstanceData

@dataclass
class TupleGraphEquivalenceMinimizerStatistics:
    num_input_tuples: int = 0
    num_output_tuples: int = 0

    def print(self):
        print("TupleGraphEquivalenceMinimizerStatistics:")
        print("    Number of input tuples:", self.num_input_tuples)
        print("    Number of output tuples:", self.num_output_tuples)


class TupleGraphEquivalenceMinimizer:
    """
    Define partial order "<" over tuples as follows:
      Given two tuples t1,t2 in T^k(s). Then t1 < t2 iff
      dist(s, t1) = dist(s, t2) and C(s, t1) subset C(s, t2)
      where C(s, t) for a tuple t is smallest set of rules
      over feature pool F that must be selected for t
      to be selected as subgoal of the subproblem rooted at s.

    Define equivalence relation "~" over tuples as follows:
      Given two tuples t1,t2 in T^k(s). Then t1 ~ t2 iff
      dist(s, t1) = dist(s, t2) and C(s, t1) = C(s, t2).

    Define tuple t in T^k(s) as satisfiable iff
    for all r in C(s, t) holds that deadend-dist(s, r) > dist(s, t).

    Then we want to prune subgoal tuples t that:
      (1) is unsatisfiable,
      (2) for which there exists a tuple t' with t' < t, and
      (3) for which there exists a representative tuple t' with t ~ t'.
    """
    def __init__(self):
        self.statistics = TupleGraphEquivalenceMinimizerStatistics()

    def minimize(self, instance_data: InstanceData):
        tuple_graph_equivalences = dict()
        for s_idx in instance_data.state_space.get_state_indices():
            tuple_graph = instance_data.tuple_graphs[s_idx]
            tuple_graph_equivalence = instance_data.tuple_graph_equivalences[s_idx]
            tuple_graph_equivalences[s_idx] = self._minimize(tuple_graph, tuple_graph_equivalence)
        return tuple_graph_equivalences

    def _minimize(self, tuple_graph: dlplan.TupleGraph, tuple_graph_equivalence: TupleGraphEquivalence):
        # compute solvable tuple nodes
        solvable_tuple_nodes = []
        for distance, tuple_nodes in enumerate(tuple_graph.get_tuple_nodes_by_distance()):
            self.statistics.num_input_tuples += len(tuple_nodes)
            for tuple_node in tuple_nodes:
                t_idx = tuple_node.get_tuple_index()
                r_idxs = frozenset(tuple_graph_equivalence.t_idx_to_r_idxs[t_idx])
                # 1. Check for satisfiability of tuple
                satisfiable = True
                for r_idx in r_idxs:
                    if tuple_graph_equivalence.r_idx_to_deadend_distance.get(r_idx, math.inf) <= distance:
                        satisfiable = False
                        break
                if not satisfiable:
                    continue
                solvable_tuple_nodes.append(tuple_node)
        # compute order
        order = defaultdict(set)
        for tuple_node_1 in solvable_tuple_nodes:
            t_idx_1 = tuple_node_1.get_tuple_index()
            r_idxs_1 = frozenset(tuple_graph_equivalence.t_idx_to_r_idxs[t_idx_1])
            for tuple_node_2 in solvable_tuple_nodes:
                t_idx_2 = tuple_node_2.get_tuple_index()
                r_idxs_2 = frozenset(tuple_graph_equivalence.t_idx_to_r_idxs[t_idx_2])
                if t_idx_1 == t_idx_2:
                    continue
                if r_idxs_1.issubset(r_idxs_2) and r_idxs_1 != r_idxs_2:
                    # t_2 gets dominated by t_1
                    order[t_idx_2].add(t_idx_1)
        # select tuple nodes according to order
        selected_t_idxs = set()
        selected_r_idxs = set()
        representative_r_idxs = set()
        for tuple_nodes in tuple_graph.get_tuple_nodes_by_distance():
            for tuple_node in tuple_nodes:
                t_idx = tuple_node.get_tuple_index()
                r_idxs = frozenset(tuple_graph_equivalence.t_idx_to_r_idxs[t_idx])
                if order.get(t_idx, 0) != 0:
                    continue
                if r_idxs in representative_r_idxs:
                    continue
                representative_r_idxs.add(r_idxs)
                # found tuple with minimal number of rules
                selected_t_idxs.add(t_idx)
                selected_r_idxs.update(r_idxs)
        self.statistics.num_output_tuples += len(selected_t_idxs)
        # print(tuple_graph.to_dot(1))
        print("Num subgoals:", len(tuple_graph_equivalence.t_idx_to_r_idxs))
        print("Num of selected subgoals:", len(selected_t_idxs))
        print("Num rules:", len(tuple_graph_equivalence.r_idx_to_distance))
        print("Num of selected rules:", len(selected_r_idxs))
        t_idx_to_r_idxs = dict()
        for t_idx, r_idxs in tuple_graph_equivalence.t_idx_to_r_idxs.items():
            if t_idx in selected_t_idxs:
                t_idx_to_r_idxs[t_idx] = [r_idx for r_idx in r_idxs if r_idx in representative_r_idxs]
        r_idx_to_deadend_distance = dict()
        t_idx_to_distance = dict()
        for t_idx, distance in tuple_graph_equivalence.t_idx_to_distance.items():
            if t_idx in selected_t_idxs:
                t_idx_to_distance[t_idx] = distance
        for r_idx, deadend_distance in tuple_graph_equivalence.r_idx_to_deadend_distance.items():
            if r_idx in selected_r_idxs:
                r_idx_to_deadend_distance[r_idx] = deadend_distance
        r_idx_to_distance = dict()
        for r_idx, distance in tuple_graph_equivalence.r_idx_to_distance.items():
            if r_idx in selected_r_idxs:
                r_idx_to_distance[r_idx] = distance
        return TupleGraphEquivalence(t_idx_to_r_idxs, t_idx_to_distance, r_idx_to_deadend_distance, r_idx_to_distance)
