import dlplan
import math

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
        for s_idx, tuple_graph in instance_data.tuple_graphs.items():
            tuple_graph_equivalence = instance_data.tuple_graph_equivalences[s_idx]
            instance_data.tuple_graphs[s_idx] = self._minimize(tuple_graph, tuple_graph_equivalence)

    def _minimize(self, tuple_graph: dlplan.TupleGraph, tuple_graph_equivalence: TupleGraphEquivalence):
        representatives = set()
        selected_t_idxs = []
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
                # 2. Check for equivalence
                if r_idxs in representatives:
                    continue
                # 3. Check for partial order
                for representative in representatives:
                    if representative.issubset(r_idxs):
                        continue
                representatives.add(r_idxs)
                selected_t_idxs.append(t_idx)
        self.statistics.num_output_tuples += len(selected_t_idxs)
        print(tuple_graph.to_dot(1))
        print("Num subgoals:", len(tuple_graph_equivalence.t_idx_to_r_idxs))
        print("Num representative r_idxs:", len(representatives))
        print("Representative r_idxs:", representatives)
        print("Representative subgoals:", selected_t_idxs)
        return TupleGraphMinimizer().restrict_tuple_graph_according_to_t_idxs(tuple_graph, selected_t_idxs)
