from clingo import String, Number

from ....iteration_data.state_pair_equivalence_data import StatePairEquivalenceData
from ....iteration_data.tuple_graph_equivalence_data import TupleGraphEquivalenceData
from ....instance_data.tuple_graph import TupleGraph

class TupleGraphFactFactory():
    def make_facts(self, instance_idx: int, tuple_graph: TupleGraph, state_pair_equivalence_data: StatePairEquivalenceData, tuple_graph_equivalence_data: TupleGraphEquivalenceData):
        if tuple_graph is None: return []
        facts = []
        facts.append(("exceed", [Number(instance_idx), Number(tuple_graph.root_idx)]))
        if tuple_graph.width == 0:
            low = 1
        else:
            low = 0
        for d in range(low, len(tuple_graph.t_idxs_by_distance)):
            for t_idx in tuple_graph.t_idxs_by_distance[d]:
                facts.append(("t_distance", [Number(instance_idx), Number(tuple_graph.root_idx), Number(t_idx), Number(d)]))
                facts.append(("tuple", [Number(instance_idx), Number(tuple_graph.root_idx), Number(t_idx)]))
                for r_idx in tuple_graph_equivalence_data.t_idx_to_r_idxs[t_idx]:
                    facts.append(("contain", [Number(instance_idx), Number(tuple_graph.root_idx), Number(t_idx), Number(r_idx)]))
        for r_idx, d in tuple_graph_equivalence_data.r_idx_to_deadend_distance.items():
            facts.append(("d_distance", [Number(instance_idx), Number(tuple_graph.root_idx), Number(r_idx), Number(d)]))
        for r_idx, state_pairs in state_pair_equivalence_data.r_idx_to_state_pairs.items():
            for (source_idx, target_idx) in state_pairs:
                if tuple_graph.width == 0 and source_idx == target_idx: continue
                facts.append(("equivalence_contains", [Number(instance_idx), Number(r_idx), Number(source_idx), Number(target_idx)]))
        return facts
