import logging
import dlplan
from typing import List
from dataclasses import dataclass
from enum import Enum
from tarski.io import PDDLReader

from ..util.command import execute, read_file
from ..util.naming import filename_core
from .transition_system import TransitionSystemFactory, TransitionSystem
from .tuple_graph import TupleGraph, TupleGraphFactory, TupleGraphMinimizer
from .return_codes import ReturnCode
from ..domain_data.domain_data import DomainData


@dataclass
class InstanceData:
    """ """
    instance_filename: str
    domain_data: DomainData
    transition_system: TransitionSystem
    tuple_graphs_by_state_index: List[TupleGraph]

    def print_statistics(self):
        self.transition_system.print_statistics()


class InstanceDataFactory:
    def make_instance_data(self, config, instance_filename, domain_data):
        logging.info(f"Constructing InstanceData for filename {instance_filename}")
        execute([config.sse_location, "--workspace", "/tmp/workspace", "--domain", domain_data.domain_filename, "--instance", instance_filename, "--options", f"max_expansions={config.max_states_per_instance},max_nodes_per_class=-1,ignore_non_fringe_dead_states=false,seed=1"], stdout=config.state_space_filename)
        instance_info = dlplan.InstanceInfo(domain_data.vocabulary_info)
        transition_system, return_code = TransitionSystemFactory().parse_transition_system(instance_info, config.state_space_filename)
        if return_code != ReturnCode.SOLVABLE:
            return None, return_code
        tuple_graphs_by_state_index = self._make_tuple_graphs(config, instance_info, transition_system)
        return InstanceData(instance_filename, domain_data, transition_system, tuple_graphs_by_state_index), ReturnCode.SOLVABLE

    def _parse_instance_file(self, domain_filename, instance_filename):
        """ Parses the PDDL instance file using Tarski. """
        reader = PDDLReader()
        reader.parse_domain(domain_filename)
        reader.parse_instance(instance_filename)
        return reader.problem

    def _make_tuple_graphs(self,
        config,
        instance_info: dlplan.InstanceInfo,
        transition_system: TransitionSystem):
        tuple_graph_factory = TupleGraphFactory(
            config, instance_info, transition_system)
        tuple_graph_minimizer = TupleGraphMinimizer()
        tuple_graphs_by_state_index = [tuple_graph_minimizer.minimize(tuple_graph_factory.make_tuple_graph(config, i)) for i in range(
            transition_system.get_num_states())]
        print("Tuple graph minimizer:")
        print(f"Num generated subgoal tuples: {tuple_graph_minimizer.num_generated}")
        print(f"Num pruned subgoal tuples: {tuple_graph_minimizer.num_pruned}")
        return tuple_graphs_by_state_index
