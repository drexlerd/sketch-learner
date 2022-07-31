from ....iteration_data.equivalence_data import TupleGraphEquivalenceData, StatePairEquivalenceData
from ....instance_data.tuple_graph import TupleGraph

class TupleGraphFactFactory():
    def make_facts(self, instance_idx: int, tuple_graph: TupleGraph, state_pair_equivalence_data: StatePairEquivalenceData, tuple_graph_equivalence_data: TupleGraphEquivalenceData):
        if tuple_graph is None: return []
        facts = set()
        facts.add(f"exceed({instance_idx},{tuple_graph.root_idx}).")
        if tuple_graph.width == 0:
            low = 1
        else:
            low = 0
        for d in range(low, len(tuple_graph.t_idxs_by_distance)):
            for t_idx in tuple_graph.t_idxs_by_distance[d]:
                facts.add(f"t_distance({instance_idx},{tuple_graph.root_idx},{t_idx},{d}).")
                facts.add(f"tuple({instance_idx},{tuple_graph.root_idx},{t_idx}).")
                for r_idx in tuple_graph_equivalence_data.t_idx_to_r_idxs[t_idx]:
                    facts.add(f"contain({instance_idx},{tuple_graph.root_idx},{t_idx},{r_idx}).")
        for r_idx, d in tuple_graph_equivalence_data.r_idx_to_deadend_distance.items():
            facts.add(f"d_distance({instance_idx},{tuple_graph.root_idx},{r_idx},{d}).")
        for r_idx, state_pairs in state_pair_equivalence_data.r_idx_to_state_pairs.items():
            for (source_idx, target_idx) in state_pairs:
                if tuple_graph.width == 0 and source_idx == target_idx: continue
                facts.add(f"equivalence_contains({instance_idx},{r_idx},{source_idx},{target_idx}).")
        return list(facts)
