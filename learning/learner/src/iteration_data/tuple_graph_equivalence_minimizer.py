import dlplan
import math

from collections import defaultdict
from typing import Dict, List, MutableSet, Tuple
from dataclasses import dataclass

from learner.src.instance_data.instance_data import InstanceData
from learner.src.iteration_data.tuple_graph_equivalence_factory import TupleGraphEquivalenceFactoryStatistics


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
        self.statistics = TupleGraphEquivalenceFactoryStatistics()

    def minimize(self, instance_data: InstanceData):
        for root_idx, tuple_graph in instance_data.tuple_graphs.items():
            if instance_data.is_deadend(root_idx):
                continue

            tuple_graph = instance_data.tuple_graphs[root_idx]
            tuple_graph_equivalence = instance_data.tuple_graph_equivalences[root_idx]
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
            for _, tuple_nodes in enumerate(tuple_graph.get_tuple_nodes_by_distance()):
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

            # restrict to selected tuples
            t_idx_to_r_idxs = defaultdict(set)
            t_idx_to_distance = dict()
            for t_idx, r_idxs in tuple_graph_equivalence.t_idx_to_r_idxs.items():
                if t_idx in selected_t_idxs:
                    t_idx_to_r_idxs[t_idx] = r_idxs
            for t_idx, distance in tuple_graph_equivalence.t_idx_to_distance.items():
                if t_idx in selected_t_idxs:
                    t_idx_to_distance[t_idx] = distance
            tuple_graph_equivalence.t_idx_to_r_idxs = t_idx_to_r_idxs
            tuple_graph_equivalence.t_idx_to_distance = t_idx_to_distance
            #tuple_graph_equivalence.print()
            self.statistics.collect_statistics(tuple_graph_equivalence)
