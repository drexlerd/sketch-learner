from typing import List, Dict

import pymimir as mm

from .instance_data import InstanceData
from .domain_data import DomainData

from ..util import change_dir, write_file


def compute_tuple_graphs(domain_data: DomainData, instance_datas: List[InstanceData], width: int, enable_dump_files: bool) -> List[Dict[int, mm.TupleGraph]]:
    """ Compute a tuple graph for each representative concrete state of each global faithful abstract state.
    """
    ss_state_idx_to_tuple_graph: List[Dict[int, mm.TupleGraph]] = []

    for instance_data in instance_datas:
        tuple_graph_factory = mm.TupleGraphFactory(instance_data.mimir_ss, width, True)

        tuple_graphs = dict()

        for mimir_ss_state_idx, mimir_ss_state in enumerate(instance_data.mimir_ss.get_states()):

            if instance_data.mimir_ss.is_deadend_state(mimir_ss_state_idx):
                continue

            tuple_graph = tuple_graph_factory.create(mimir_ss_state.get_state())
            tuple_graphs[mimir_ss_state_idx] = tuple_graph

            with change_dir(f"tuple_graphs/{instance_data.idx}/{mimir_ss_state_idx}", enable=enable_dump_files):
                if enable_dump_files:
                    write_file(f"{mimir_ss_state_idx}.dot", str(tuple_graph))

        ss_state_idx_to_tuple_graph.append(tuple_graphs)

    return ss_state_idx_to_tuple_graph
