from typing import List

from dlplan.novelty import NoveltyBase, TupleGraph

from learner.src.instance_data.instance_data import InstanceData
from learner.src.instance_data.tuple_graph import PerStateTupleGraphs


def compute_tuple_graphs(width: int, instance_datas: List[InstanceData]):
    for instance_data in instance_datas:
        per_state_tuple_graphs = PerStateTupleGraphs()
        novelty_base = NoveltyBase(len(instance_data.state_space.get_instance_info().get_atoms()), width)
        for s_idx in instance_data.state_space.get_states().keys():
            if instance_data.is_deadend(s_idx):
                continue
            per_state_tuple_graphs.s_idx_to_tuple_graph[s_idx] = TupleGraph(novelty_base, instance_data.state_space, s_idx, True)
        instance_data.set_per_state_tuple_graphs(per_state_tuple_graphs)