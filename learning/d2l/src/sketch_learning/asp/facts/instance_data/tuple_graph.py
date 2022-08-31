from clingo import String, Number

from ....iteration_data.state_pair_equivalence import StatePairEquivalence
from ....iteration_data.tuple_graph_equivalence import TupleGraphEquivalence
from ....instance_data.tuple_graph import TupleGraph


class TupleGraphFactFactory():
    def make_facts(self, instance_idx: int, tuple_graph: TupleGraph, state_pair_equivalence: StatePairEquivalence, tuple_graph_equivalence: TupleGraphEquivalence):
        if tuple_graph is None: return []
        facts = []
        facts.append(("exceed", [Number(instance_idx), Number(tuple_graph.root_idx)]))
        for d in range(len(tuple_graph.t_idxs_by_distance)):
            for t_idx in tuple_graph.t_idxs_by_distance[d]:
                facts.append(("t_distance", [Number(instance_idx), Number(tuple_graph.root_idx), Number(t_idx), Number(d)]))
                facts.append(("tuple", [Number(instance_idx), Number(tuple_graph.root_idx), Number(t_idx)]))
                for r_idx in tuple_graph_equivalence.t_idx_to_r_idxs[t_idx]:
                    facts.append(("contain", [Number(instance_idx), Number(tuple_graph.root_idx), Number(t_idx), Number(r_idx)]))
        for r_idx, d in tuple_graph_equivalence.r_idx_to_deadend_distance.items():
            facts.append(("d_distance", [Number(instance_idx), Number(tuple_graph.root_idx), Number(r_idx), Number(d)]))
        for r_idx, d in tuple_graph_equivalence.r_idx_to_distance.items():
            facts.append(("r_distance", [Number(instance_idx), Number(tuple_graph.root_idx), Number(r_idx), Number(d)]))
            if d == 0:
                facts.append(("looping_equivalences", (Number(r_idx),)))
        for r_idx, state_pairs in state_pair_equivalence.r_idx_to_state_pairs.items():
            for state_pair in state_pairs:
                facts.append(("equivalence_contains", [Number(instance_idx), Number(r_idx), Number(state_pair.source_idx), Number(state_pair.target_idx)]))
        return facts
