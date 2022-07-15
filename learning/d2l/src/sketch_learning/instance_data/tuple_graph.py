import dlplan
from collections import defaultdict
from typing import Dict, List, MutableSet
from dataclasses import dataclass, field

from .transition_system import TransitionSystem
from .novelty_table import NoveltyTable


@dataclass
class TupleGraph:
    def __init__(self,
        root_idx: int,
        t_idxs_by_distance: List[List[int]],
        s_idxs_by_distance: List[List[int]],
        t_idx_to_s_idxs: Dict[int, MutableSet[int]],
        s_idx_to_t_idxs: Dict[int, MutableSet[int]],
        width: int):
        assert len(s_idxs_by_distance) == len(t_idxs_by_distance)
        self.root_idx = root_idx
        self.width = width
        self.t_idxs_by_distance = t_idxs_by_distance
        self.s_idxs_by_distance = s_idxs_by_distance
        self.t_idx_to_s_idxs = t_idx_to_s_idxs
        self.s_idx_to_t_idxs = s_idx_to_t_idxs

    def exists_admissible_chain_for(self, s_idxs : MutableSet[int]):
        """ Returns true iff there exists an admissible chain for s_idxs. """
        for s_idxs_2 in self.t_idx_to_s_idxs.values():
            if all(s_idx in s_idxs for s_idx in s_idxs_2):
                return True
        return False

    def print(self):
        print(f"Tuple graph for state {self.root_idx} and width {self.width}")
        print(f"t_idxs_by_distance: {self.t_idxs_by_distance}")
        print(f"s_idxs_by_distance: {self.s_idxs_by_distance}")
        print(f"t_idx_to_s_idxs: {self.t_idx_to_s_idxs}")
        print(f"s_idx_to_t_idxs: {self.s_idx_to_t_idxs}")


class TupleGraphFactory:
    def __init__(self,
        config,
        instance_info: dlplan.InstanceInfo,
        transition_system: TransitionSystem):
        self.transition_system = transition_system
        self.width = config.width
        # dynamic atoms must follow indexing scheme to make the tuple index computation work.
        dynamic_dlplan_atoms = [atom for atom in instance_info.get_atoms() if not atom.get_is_static()]
        assert all([atom.get_index() in range(len(dynamic_dlplan_atoms)) for atom in dynamic_dlplan_atoms])
        self.num_dynamic_atoms = len(dynamic_dlplan_atoms)
        # we only care about atom indices in each state.
        self.dynamic_atoms_per_state_index = [[atom_idx for atom_idx in dlplan_state.get_atom_idxs() if not instance_info.get_atom(atom_idx).get_is_static()]
            for dlplan_state in transition_system.states_by_index]

    def make_tuple_graph(self, config, source_index: int):
        if self.transition_system.is_goal(source_index) \
            or self.transition_system.is_deadend(source_index) \
            or config.tuple_graph_if_width_exceeds: return None
        if self.width == 0:
            return self._make_tuple_graph_for_width_0(source_index)
        else:
            return self._make_tuple_graph_for_width_greater_0(source_index)

    def _make_tuple_graph_for_width_0(self, source_index: int):
        """ Special case where each 1-step successor can be a subgoal. """
        s_idxs_by_distance = [[source_index], list(self.transition_system.forward_transitions[source_index])]
        # we use state indices also for tuples for simplicity
        t_idxs_by_distance = [[source_index], list(self.transition_system.forward_transitions[source_index])]
        t_idx_to_s_idxs = defaultdict(set)
        s_idx_to_t_idxs = defaultdict(set)
        t_idx_to_s_idxs[source_index].add(source_index)
        for suc_index in self.transition_system.forward_transitions[source_index]:
            t_idx_to_s_idxs[suc_index].add(suc_index)
            s_idx_to_t_idxs[suc_index].add(suc_index)
        return TupleGraph(source_index, t_idxs_by_distance, s_idxs_by_distance, t_idx_to_s_idxs, s_idx_to_t_idxs, self.width)

    def _make_tuple_graph_for_width_greater_0(self, source_index):
        """ Constructing tuple graph for width greater 0 as defined in the literature. """
        novelty_table = NoveltyTable(self.width, self.num_dynamic_atoms)
        # states s[pi] by distance for optimal plan pi in Pi^*(t).
        s_idxs_by_distance = self.transition_system.compute_states_by_distance(source_index)
        # information of tuples during computation
        t_idx_to_s_idxs = defaultdict(set)
        s_idx_to_t_idxs = dict()
        # information of tuples that make it into the tuple graph
        marked_t_idxs_by_distance = []
        marked_t_idx_to_s_idxs = defaultdict(set)
        marked_s_idx_to_t_idxs = defaultdict(set)
        for d, s_idxs_in_layer in enumerate(s_idxs_by_distance):
            novel_t_idxs_in_current_layer = self._find_novel_tuples_in_layer(s_idxs_in_layer, novelty_table, t_idx_to_s_idxs, s_idx_to_t_idxs)
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
                marked_t_idxs_in_current_layer = self._extend_optimal_plans(marked_t_idxs_by_distance[d-1], novel_t_idxs_in_current_layer, t_idx_to_s_idxs, s_idx_to_t_idxs)
                if not marked_t_idxs_in_current_layer: break  # nothing to keep extending
                # store information of marked tuples
                marked_t_idxs_by_distance.append(marked_t_idxs_in_current_layer)
                for t_idx in marked_t_idxs_in_current_layer:
                    marked_t_idx_to_s_idxs[t_idx] = t_idx_to_s_idxs[t_idx]
                    for s_idx in t_idx_to_s_idxs[t_idx]:
                        marked_s_idx_to_t_idxs[s_idx].add(t_idx)
        assert d > 1
        return TupleGraph(source_index, marked_t_idxs_by_distance, s_idxs_by_distance[:len(marked_t_idxs_by_distance)], marked_t_idx_to_s_idxs, marked_s_idx_to_t_idxs, self.width)

    def _find_novel_tuples_in_layer(self, s_idxs_in_layer: List[int], novelty_table: NoveltyTable, t_idx_to_s_idxs, s_idx_to_t_idxs) -> List[int]:
        """ Given a list of states `s_idxs_in_layer`
            return all tuple indices that are novel in at least one state.  """
        t_idxs = set()  # the novel tuples with distance d
        for s_idx in s_idxs_in_layer:
            t_idxs_for_s_idx = novelty_table.compute_novel_t_idxs(self.dynamic_atoms_per_state_index[s_idx])
            if t_idxs_for_s_idx:
                # S*(s, t)
                s_idx_to_t_idxs[s_idx] = t_idxs_for_s_idx
                t_idxs.update(t_idxs_for_s_idx)
                for t_idx in t_idxs_for_s_idx:
                    t_idx_to_s_idxs[t_idx].add(s_idx)
        return t_idxs

    def _extend_optimal_plans(self, marked_t_idxs_in_previous_layer: List[int], novel_t_idxs_in_current_layer: List[int], t_idx_to_s_idxs, s_idx_to_t_idxs) -> List[int]:
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
                for sj_idx in self.transition_system.forward_transitions[si_idx]:
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


class TupleGraphMinimizer:
    """ Restrict the tuple graph to minimal elements according to the partial ordering "<",
    where t1 < t2, if S*(s, t1) subseteq S*(s, t2). """
    def __init__(self):
        self.num_generated = 0
        self.num_pruned = 0

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
        self.num_generated += len(t_idx_to_s_idxs)
        self.num_pruned += len(tuple_graph.t_idx_to_s_idxs) - len(t_idx_to_s_idxs)
        return TupleGraph(tuple_graph.root_idx, t_idxs_by_distance, tuple_graph.s_idxs_by_distance, t_idx_to_s_idxs, s_idx_to_t_idxs, tuple_graph.width)

    def minimize(self, tuple_graph: TupleGraph):
        if tuple_graph is None: return None
        succ_order = self._compute_tuple_ordering(tuple_graph)
        selected_t_idxs = self._compute_unique_maximal_elements_according_to_ordering(tuple_graph, succ_order)
        tuple_graph = self._restrict_tuple_graph_according_to_unique_maximal_elements(tuple_graph, selected_t_idxs)
        return tuple_graph
