from ....iteration_data.equivalence_data import TupleGraphExt


class TupleGraphFactFactory():
    def make_facts(self, instance_idx: int, tuple_graph_ext: TupleGraphExt):
        if tuple_graph_ext is None: return []
        facts = []
        facts.append(f"exceed({instance_idx},{tuple_graph_ext.root_idx}).")
        if tuple_graph_ext.width == 0:
            low = 1
        else:
            low = 0
        for d in range(low, len(tuple_graph_ext.t_idxs_by_distance)):
            for t_idx in tuple_graph_ext.t_idxs_by_distance[d]:
                facts.append(f"t_distance({instance_idx},{tuple_graph_ext.root_idx},{t_idx},{d}).")
                facts.append(f"tuple({instance_idx},{tuple_graph_ext.root_idx},{t_idx}).")
                for r_idx in tuple_graph_ext.t_idx_to_r_idxs[t_idx]:
                    facts.append(f"contain({instance_idx},{tuple_graph_ext.root_idx},{t_idx},{r_idx}).")
        for r_idx, d in tuple_graph_ext.r_idx_to_deadend_distance.items():
            facts.append(f"d_distance({instance_idx},{tuple_graph_ext.root_idx},{r_idx},{d}).")
        for r_idx, s_idxs in tuple_graph_ext.r_idx_to_s_idxs.items():
            for s_idx in s_idxs:
                if tuple_graph_ext.width == 0 and s_idx in tuple_graph_ext.s_idxs_by_distance[0]: continue
                facts.append(f"equivalence_contains({instance_idx},{r_idx},{tuple_graph_ext.root_idx},{s_idx}).")
        return facts
