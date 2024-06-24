from typing import List, Dict

import pymimir as mm

from .instance_data import InstanceData, StateFinder
from ..domain_data.domain_data import DomainData

from ..util.command import change_dir, write_file


def compute_tuple_graphs(domain_data: DomainData, instance_datas: List[InstanceData], state_finder: StateFinder, width: int, enable_dump_files: bool):
    """ Compute a tuple graph for each representative concrete state of each global faithful abstract state.
    """
    gfa_state_id_to_tuple_graph: Dict[int, mm.TupleGraph] = dict()

    tuple_graph_factories = []
    for instance_data in instance_datas:
        tuple_graph_factories.append(mm.TupleGraphFactory(instance_data.mimir_ss, width, True))

    for instance_data in instance_datas:
        gfa = instance_data.gfa

        for gfa_state_idx, gfa_state in enumerate(instance_data.gfa.get_states()):
            if gfa.is_deadend_state(gfa_state_idx):
                continue

            tuple_graph_factory = tuple_graph_factories[gfa_state.get_abstraction_index()]
            ss_state = state_finder.get_mimir_ss_state(gfa_state)
            tuple_graph = tuple_graph_factory.create(ss_state)

            gfa_state_id = gfa_state.get_id()
            gfa_state_id_to_tuple_graph[gfa_state_id] = tuple_graph

            with change_dir(f"tuple_graphs/{instance_data.idx}/{gfa_state_idx}", enable=enable_dump_files):
                if enable_dump_files:
                    write_file(f"{gfa_state_idx}.dot", str(tuple_graph))

    domain_data.gfa_state_id_to_tuple_graph = gfa_state_id_to_tuple_graph
