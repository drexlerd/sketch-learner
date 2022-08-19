from collections import defaultdict
from dataclasses import dataclass

from .tuple_graph import TupleGraph

@dataclass
class Statistics:
    num_generated: int = 0
    num_pruned: int = 0

    def print(self):
        print("Number of generated tuples:", self.num_generated)
        print("Number of pruned tuples:", self.num_pruned)


class TupleGraphMinimizer:
    """ Restrict the tuple graph to minimal elements according to the partial ordering "<",
    where t1 < t2, if S*(s, t1) subseteq S*(s, t2). """
    def __init__(self):
        self.statistics = Statistics()

    def minimize(self, tuple_graph: TupleGraph):
        if tuple_graph is None:
            return None
        succ_order = self._compute_tuple_ordering(tuple_graph)
        selected_t_idxs = self._compute_unique_maximal_elements_according_to_ordering(tuple_graph, succ_order)
        tuple_graph = self._restrict_tuple_graph_according_to_unique_maximal_elements(tuple_graph, selected_t_idxs)
        return tuple_graph

    def _compute_tuple_ordering(self, tuple_graph: TupleGraph):
        """ ti > tj, i.e., ti in succ_order[tj] if S*(s,ti) is strict subset of S*(s,tj)
        """
        succ_order = defaultdict(set)
        for t_idxs in tuple_graph.t_idxs_by_distance:
            for ti_idx in t_idxs:
                si_idxs = tuple_graph.t_idx_to_s_idxs[ti_idx]
                for tj_idx in t_idxs:
                    if ti_idx == tj_idx: continue
                    sj_idxs = tuple_graph.t_idx_to_s_idxs[tj_idx]
                    if si_idxs == sj_idxs: continue
                    if si_idxs.issubset(sj_idxs):  # ti > tj
                        succ_order[tj_idx].add(ti_idx)
        return succ_order

    def _compute_unique_maximal_elements_according_to_ordering(self, tuple_graph: TupleGraph, succ_order):
        """
        """
        selected_s_idxs = set()
        selected_t_idxs = set()
        for t_idx, s_idxs in tuple_graph.t_idx_to_s_idxs.items():
            if len(succ_order[t_idx]) == 0:
                canonical_s_idxs = tuple(sorted(list(s_idxs)))
                if canonical_s_idxs not in selected_s_idxs:
                    selected_s_idxs.add(canonical_s_idxs)
                    selected_t_idxs.add(t_idx)
        return selected_t_idxs

    def _restrict_tuple_graph_according_to_unique_maximal_elements(self, tuple_graph: TupleGraph, selected_t_idxs):
        t_idxs_by_distance = []
        for t_idxs in tuple_graph.t_idxs_by_distance:
            t_idxs_by_distance.append([t_idx for t_idx in t_idxs if t_idx in selected_t_idxs])
        t_idx_to_s_idxs = dict()
        s_idx_to_t_idxs = defaultdict(set)
        for t_idx in selected_t_idxs:
            t_idx_to_s_idxs[t_idx] = tuple_graph.t_idx_to_s_idxs[t_idx]
            for s_idx in t_idx_to_s_idxs[t_idx]:
                s_idx_to_t_idxs[s_idx].add(t_idx)
        self.statistics.num_generated += len(t_idx_to_s_idxs)
        self.statistics.num_pruned += len(tuple_graph.t_idx_to_s_idxs) - len(t_idx_to_s_idxs)
        return TupleGraph(tuple_graph.novelty_base, tuple_graph.root_idx, t_idxs_by_distance, tuple_graph.s_idxs_by_distance, t_idx_to_s_idxs, s_idx_to_t_idxs, tuple_graph.width)
