from typing import List, Dict

import pymimir as mm

from .state_finder import StateFinder
from .instance_data import InstanceData
from .domain_data import DomainData

from ..util import change_dir, write_file


def compute_tuple_graphs(domain_data: DomainData, instance_datas: List[InstanceData], state_finder: StateFinder, width: int, enable_dump_files: bool):
    """ Compute a tuple graph for each representative concrete state of each global faithful abstract state.
    """
    gfa_state_global_idx_to_tuple_graph: Dict[int, mm.TupleGraph] = dict()

    tuple_graph_factories = []
    for instance_data in instance_datas:
        tuple_graph_factories.append(mm.TupleGraphFactory(instance_data.mimir_ss, width, True))

    for instance_data in instance_datas:
        gfa = instance_data.gfa

        for gfa_state in instance_data.gfa.get_states():

            if gfa.is_deadend_state(gfa_state.get_index()):
                continue

            if gfa_state.get_global_index() in gfa_state_global_idx_to_tuple_graph:
                continue

            tuple_graph_factory = tuple_graph_factories[gfa_state.get_faithful_abstraction_index()]
            ss_state = state_finder.get_mimir_ss_state(gfa_state)
            tuple_graph = tuple_graph_factory.create(ss_state)
            gfa_state_global_idx_to_tuple_graph[gfa_state.get_global_index()] = tuple_graph

            with change_dir(f"tuple_graphs/{instance_data.idx}/{gfa_state.get_index()}", enable=enable_dump_files):
                if enable_dump_files:
                    write_file(f"{gfa_state.get_index()}.dot", str(tuple_graph))

    return gfa_state_global_idx_to_tuple_graph
