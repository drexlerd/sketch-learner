import dlplan
from collections import defaultdict
from typing import Dict, List, MutableSet
from dataclasses import dataclass, field

from .transition_system import TransitionSystem
from .novelty_table import NoveltyTable


@dataclass
class TupleGraph:
    """ Our definition of a TupleGraph is slightly different from the literature
        in the sense that they are equivalent but the representation is more compact.
        The differences are:
            1. There is only a single root node representing an arbitrary
               tuple of atoms t0 that is true in the initial state.
            2. Two tuple of atoms ti,ti' are equivalent, i.e., t1~t2,
               iff the sets of states underlying ti and ti' are identical.

        Proof sketches that (1) and (2) can be used to simplify the representation:
        Regarding (1), we can observe that any tuple that is true in the initial
        state is extended to the same tuples as defined in part 2 of the definition of width.
        Regarding (2), when extending a tuple as defined in part 2 of the definition of width,
        one has to extend the underlieing optimal plans which are identical for ti,ti'
        if the underlying states are identical.
        Note: using subset relation on the underlying states in the definition of equivalence classes
        does not work because it is asymmetric, i.e., tuple with fewer underlying states
        can be extended into successor tuple with more underlying states and vice versa.
    """
    root_idx: int
    t_idxs_by_distance: List[List[int]]
    s_idxs_by_distance: List[List[int]]
    t_idx_to_s_idxs: Dict[int, MutableSet]
    width: int

    def exists_admissible_chain_for(self, s_idxs : MutableSet[int]):
        """ Returns true iff there exists an admissible chain for s_idxs. """
        for s_idxs_2 in self.t_idx_to_s_idxs.values():
            if all(s_idx in s_idxs for s_idx in s_idxs_2):
                return True
        return False

    def print(self):
        print(self.t_idxs_by_distance)
        print(self.s_idxs_by_distance)
        print(self.t_idx_to_s_idxs)


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

    def make_tuple_graph(self, config, source_index):
        if self.transition_system.is_goal(source_index) \
            or self.transition_system.is_deadend(source_index) \
            or config.tuple_graph_if_width_exceeds: return None
        if self.width == 0:
            return self._make_tuple_graph_for_width_0(source_index)
        else:
            return self._make_tuple_graph_for_width_greater_0(source_index)

    def _make_tuple_graph_for_width_0(self, source_index):
        """ Special case where each 1-step successor can be a subgoal. """
        s_idxs_by_distance = [[source_index], list(self.transition_system.forward_transitions[source_index])]
        # we use state indices also for tuples for simplicity
        t_idxs_by_distance = [[source_index], list(self.transition_system.forward_transitions[source_index])]
        t_idx_to_s_idxs = defaultdict(set)
        t_idx_to_s_idxs[source_index].add(source_index)
        for suc_index in self.transition_system.forward_transitions[source_index]:
            t_idx_to_s_idxs[suc_index].add(suc_index)
        return TupleGraph(source_index, t_idxs_by_distance, s_idxs_by_distance, t_idx_to_s_idxs, self.width)

    def _make_tuple_graph_for_width_greater_0(self, source_index):
        """ Constructing tuple graph for width greater 0 as defined in the literature. """
        novelty = NoveltyTable(self.width, self.num_dynamic_atoms)
        # S*(s, t)
        # mapping from tuple t to underlying states s[pi] for which there
        # exists some optimal plan pi in Pi^*(t).
        t_idx_to_s_idxs = defaultdict(set)
        s_idx_to_t_idxs = dict()
        # tuples t by distance.
        t_idxs_by_distance = []
        # states s[pi] by distance for optimal plan pi in Pi^*(t).
        s_idxs_by_distance = self.transition_system.compute_states_by_distance(source_index)
        # tuples t by distance that make it into the tuple graph.
        marked_t_idxs_by_distance = []
        d = 0
        for layer in s_idxs_by_distance:
            # find novel tuples for current state layer
            t_idxs = set()  # the novel tuples with distance d
            for s_idx in layer:
                t_idxs_for_s_idx = novelty.compute_novel_t_idxs(self.dynamic_atoms_per_state_index[s_idx])
                if t_idxs_for_s_idx:
                    # S*(s, t)
                    s_idx_to_t_idxs[s_idx] = t_idxs_for_s_idx
                    t_idxs.update(t_idxs_for_s_idx)
                    for t_idx in t_idxs_for_s_idx:
                        t_idx_to_s_idxs[t_idx].add(s_idx)
            if not t_idxs:
                break  # no more novel tuples
            else:
                # Note that novely is not based on the tuples that we extended
                # but rather on all tuples at smallest distance
                t_idxs_by_distance.append(t_idxs)
                novelty.mark_as_not_novel(t_idxs)
                # extend all optimal plans for ti into optimal plans for tj
                if d == 0:
                    # part (1) of definition:
                    # all tuples of the initial state make it into the tuple graph.
                    marked_t_idxs_by_distance.append(t_idxs_by_distance[0])
                else:
                    # part (2) of definition:
                    # must extend all optimal plans
                    marked_t_idxs = set()
                    extended = defaultdict(set)
                    for ti_idx in marked_t_idxs_by_distance[d-1]:
                        for si_idx in t_idx_to_s_idxs[ti_idx]:
                            for sj_idx in self.transition_system.forward_transitions[si_idx]:
                                for tj_idx in s_idx_to_t_idxs.get(sj_idx, []):
                                    # optimal plan that ends in si_idx underlying ti is
                                    # extended into optimal plan that ends in sj_idx underlying tj
                                    extended[(ti_idx, tj_idx)].add(si_idx)
                        for tj_idx in t_idxs_by_distance[d]:
                            assert len(extended[(ti_idx, tj_idx)]) <= len(t_idx_to_s_idxs[ti_idx])
                            if len(extended[(ti_idx, tj_idx)]) == len(t_idx_to_s_idxs[ti_idx]):
                                # all optimal plans for ti can be extended into an optimal plan for tj
                                marked_t_idxs.add(tj_idx)
                    if not marked_t_idxs:
                        break  # nothing to keep extending
                    else:
                        marked_t_idxs_by_distance.append(marked_t_idxs)
                d += 1
        assert d > 1
        return TupleGraph(source_index, t_idxs_by_distance, s_idxs_by_distance[:d], t_idx_to_s_idxs, self.width)

    def print_statistics(self):
        print(f"Generated tuple graph nodes: {self.generated_nodes}")
        print(f"Pruned tuple graph nodes by equivalence: {self.pruned_nodes_by_equivalence}")


class TupleGraphMinimizer:
    """ Restrict the tuple graph to minimal elements according to the partial ordering "<",
    where t1 < t2, if S*(s, t1) subseteq S*(s, t2). """
    def __init__(self):
        self.num_generated = 0
        self.num_pruned = 0

    def minimize(self, tuple_graph: TupleGraph):
        if tuple_graph is None:
            return None
        # tuple_graph.print()
        # 1. tj in succ_order[ti] if S*(s,ti) is strict subset of S*(s,tj)
        succ_order = defaultdict(set)
        for t_idxs in tuple_graph.t_idxs_by_distance:
            for ti_idx in t_idxs:
                si_idxs = tuple_graph.t_idx_to_s_idxs[ti_idx]
                for tj_idx in t_idxs:
                    if ti_idx == tj_idx: continue
                    sj_idxs = tuple_graph.t_idx_to_s_idxs[tj_idx]
                    if si_idxs == sj_idxs: continue
                    if si_idxs.issubset(sj_idxs):  # ti < tj
                        succ_order[tj_idx].add(ti_idx)
        # 2. Compute a minimal set of elements according to succ
        selected_s_idxs = set()
        selected_t_idx = set()
        for t_idx, s_idxs in tuple_graph.t_idx_to_s_idxs.items():
            if len(succ_order[t_idx]) == 0:
                canonical_s_idxs = tuple(sorted(list(s_idxs)))
                if canonical_s_idxs not in selected_s_idxs:
                    selected_s_idxs.add(canonical_s_idxs)
                    selected_t_idx.add(t_idx)
        t_idxs_by_distance = []
        t_idx_to_s_idxs = dict()
        for t_idxs in tuple_graph.t_idxs_by_distance:
            t_idxs_by_distance.append([t_idx for t_idx in t_idxs if t_idx in selected_t_idx])
        t_idx_to_s_idxs = dict()
        for t_idx in selected_t_idx:
            t_idx_to_s_idxs[t_idx] = tuple_graph.t_idx_to_s_idxs[t_idx]
        self.num_generated += len(t_idx_to_s_idxs)
        self.num_pruned += len(tuple_graph.t_idx_to_s_idxs) - len(t_idx_to_s_idxs)
        return TupleGraph(tuple_graph.root_idx, t_idxs_by_distance, tuple_graph.s_idxs_by_distance, t_idx_to_s_idxs, tuple_graph.width)
