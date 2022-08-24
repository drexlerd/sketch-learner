from collections import defaultdict
from typing import List

from .instance_data import InstanceData
from .novelty_base import NoveltyBase
from .novelty_table import NoveltyTable
from .tuple_graph import TupleGraph

from .tuple_graph_minimizer import TupleGraphMinimizer


class TupleGraphFactory:
    def __init__(self, width: int):
        self.width = width

    def make_tuple_graphs(self, instance_data: InstanceData):
        tuple_graphs = [self.make_tuple_graph(instance_data, i) for i in range(
            instance_data.transition_system.get_num_states())]
        return tuple_graphs

    def make_tuple_graph(self, instance_data: InstanceData, source_index: int):
        if instance_data.transition_system.is_goal(source_index) \
            or instance_data.transition_system.is_deadend(source_index):
            return None
        if self.width == 0:
            return self._make_tuple_graph_for_width_0(instance_data, source_index)
        else:
            return self._make_tuple_graph_for_width_greater_0(instance_data, source_index)

    def _make_tuple_graph_for_width_0(self, instance_data: InstanceData, source_index: int):
        """ Special case where each 1-step successor can be a subgoal. """
        novelty_base = NoveltyBase(self.width, instance_data.instance_info.get_atoms())
        s_idxs_by_distance = [[source_index], list(instance_data.transition_system.forward_transitions[source_index])]
        # we use state indices also for tuples for simplicity
        t_idxs_by_distance = [[source_index], list(instance_data.transition_system.forward_transitions[source_index])]
        t_idx_to_s_idxs = defaultdict(set)
        s_idx_to_t_idxs = defaultdict(set)
        t_idx_to_s_idxs[source_index].add(source_index)
        for suc_index in instance_data.transition_system.forward_transitions[source_index]:
            t_idx_to_s_idxs[suc_index].add(suc_index)
            s_idx_to_t_idxs[suc_index].add(suc_index)
        return TupleGraph(novelty_base, source_index, t_idxs_by_distance, s_idxs_by_distance, t_idx_to_s_idxs, s_idx_to_t_idxs, self.width)

    def _make_tuple_graph_for_width_greater_0(self, instance_data: InstanceData, source_index: int):
        """ Constructing tuple graph for width greater 0 as defined in the literature. """
        novelty_base = NoveltyBase(self.width, instance_data.instance_info.get_atoms())
        novelty_table = NoveltyTable(novelty_base)
        # states s[pi] by distance for optimal plan pi in Pi^*(t).
        s_idxs_by_distance, _ = instance_data.transition_system.partition_states_by_distance(states=[source_index], forward=True, stop_upon_goal=True)
        # information of tuples during computation
        t_idx_to_s_idxs = defaultdict(set)
        s_idx_to_t_idxs = dict()
        # information of tuples that make it into the tuple graph
        marked_t_idxs_by_distance = []
        marked_t_idx_to_s_idxs = defaultdict(set)
        marked_s_idx_to_t_idxs = defaultdict(set)
        for d, s_idxs_in_layer in enumerate(s_idxs_by_distance):
            novel_t_idxs_in_current_layer = self._find_novel_tuples_in_layer(instance_data, s_idxs_in_layer, novelty_table, t_idx_to_s_idxs, s_idx_to_t_idxs)
            novelty_table.mark_as_not_novel(novel_t_idxs_in_current_layer)
            if not novel_t_idxs_in_current_layer: break  # no more novel tuples
            if d == 0:
                # part (1) of definition:
                # all tuples of the initial state make it into the tuple graph.
                marked_t_idxs_by_distance.append(novel_t_idxs_in_current_layer)
                for t_idx in novel_t_idxs_in_current_layer:
                    marked_t_idx_to_s_idxs[t_idx] = t_idx_to_s_idxs[t_idx]
                    for s_idx in t_idx_to_s_idxs[t_idx]:
                        marked_s_idx_to_t_idxs[s_idx].add(t_idx)
            else:
                # part (2) of definition:
                # must extend all optimal plans
                marked_t_idxs_in_current_layer = self._extend_optimal_plans(instance_data, marked_t_idxs_by_distance[d-1], novel_t_idxs_in_current_layer, t_idx_to_s_idxs, s_idx_to_t_idxs)
                if not marked_t_idxs_in_current_layer: break  # nothing to keep extending
                # store information of marked tuples
                marked_t_idxs_by_distance.append(marked_t_idxs_in_current_layer)
                for t_idx in marked_t_idxs_in_current_layer:
                    marked_t_idx_to_s_idxs[t_idx] = t_idx_to_s_idxs[t_idx]
                    for s_idx in t_idx_to_s_idxs[t_idx]:
                        marked_s_idx_to_t_idxs[s_idx].add(t_idx)
        assert d > 0
        return TupleGraph(novelty_base, source_index, marked_t_idxs_by_distance, s_idxs_by_distance[:len(marked_t_idxs_by_distance)], marked_t_idx_to_s_idxs, marked_s_idx_to_t_idxs, self.width)

    def _find_novel_tuples_in_layer(self, instance_data: InstanceData, s_idxs_in_layer: List[int], novelty_table: NoveltyTable, t_idx_to_s_idxs, s_idx_to_t_idxs) -> List[int]:
        """ Given a list of states `s_idxs_in_layer`
            return all tuple indices that are novel in at least one state.  """
        t_idxs = set()  # the novel tuples with distance d
        for s_idx in s_idxs_in_layer:
            atom_idxs = instance_data.transition_system.s_idx_to_dlplan_state[s_idx].get_atom_idxs()
            t_idxs_for_s_idx = novelty_table.compute_novel_tuples(atom_idxs)
            if t_idxs_for_s_idx:
                # S*(s, t)
                s_idx_to_t_idxs[s_idx] = t_idxs_for_s_idx
                t_idxs.update(t_idxs_for_s_idx)
                for t_idx in t_idxs_for_s_idx:
                    t_idx_to_s_idxs[t_idx].add(s_idx)
        return t_idxs

    def _extend_optimal_plans(self, instance_data: InstanceData, marked_t_idxs_in_previous_layer: List[int], novel_t_idxs_in_current_layer: List[int], t_idx_to_s_idxs, s_idx_to_t_idxs) -> List[int]:
        """ Given a list of tuples that make it in previous layer of the tuple graph `marked_t_idxs_in_previous_layer`
            return the subset of tuples `marked_t_idxs`
            that are novel in current layer `novel_t_idxs_in_current_layer`
            such that for each tuple t' in `marked_t_idxs`
            there exists a tuple t in `novel_t_idxs_in_current_layer`
            and all optimal plans for t can be extended into an optimal plan for t'
        """
        marked_t_idxs = set()
        extended = defaultdict(set)
        for ti_idx in marked_t_idxs_in_previous_layer:
            for si_idx in t_idx_to_s_idxs[ti_idx]:
                for sj_idx in instance_data.transition_system.forward_transitions[si_idx]:
                    for tj_idx in s_idx_to_t_idxs.get(sj_idx, []):
                        # optimal plan that ends in si_idx underlying ti is
                        # extended into optimal plan that ends in sj_idx underlying tj
                        extended[(ti_idx, tj_idx)].add(si_idx)
            for tj_idx in novel_t_idxs_in_current_layer:
                assert len(extended[(ti_idx, tj_idx)]) <= len(t_idx_to_s_idxs[ti_idx])
                if len(extended[(ti_idx, tj_idx)]) == len(t_idx_to_s_idxs[ti_idx]):
                    # all optimal plans for ti can be extended into an optimal plan for tj
                    marked_t_idxs.add(tj_idx)
        return marked_t_idxs
