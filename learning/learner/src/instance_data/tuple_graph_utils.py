from typing import List

import pymimir as mm

from .instance_data import InstanceData
from .tuple_graph import PerStateTupleGraphs

from ..util.command import change_dir, write_file


def compute_tuple_graphs(width: int, instance_datas: List[InstanceData], enable_dump_files: bool):
    for instance_data in instance_datas:
        per_state_tuple_graphs = PerStateTupleGraphs()
        # TODO change pruning from False to True
        tuple_graph_factory = mm.TupleGraphFactory(instance_data.mimir_state_space, width, False)
        for s_idx, state in enumerate(instance_data.mimir_state_space.get_states()):
            if instance_data.is_deadend(s_idx):
                continue

            with change_dir(f"tuple_graphs/{instance_data.id}/{s_idx}", enable=enable_dump_files):

                tuple_graph = tuple_graph_factory.create(state)
                per_state_tuple_graphs.s_idx_to_tuple_graph[s_idx] = tuple_graph

                if enable_dump_files:
                    write_file(f"{s_idx}.dot", str(tuple_graph))

        instance_data.per_state_tuple_graphs = per_state_tuple_graphs
