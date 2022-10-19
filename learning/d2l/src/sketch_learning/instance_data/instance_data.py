import dlplan
from dataclasses import dataclass
from typing import List

from .instance_information import InstanceInformation
from .iteration_information import IterationInformation

from ..util.command import write_file
from ..domain_data.domain_data import DomainData
from ..iteration_data.feature_valuations import FeatureValuation
from ..iteration_data.state_equivalence import InstanceStateEquivalence
from ..iteration_data.state_pair_equivalence import InstanceStatePairEquivalence
from ..iteration_data.tuple_graph_equivalence import TupleGraphEquivalence
from ..driver import Bunch


@dataclass
class InstanceData:
    """ """
    id: int
    domain_data: DomainData
    denotations_caches: dlplan.DenotationsCaches
    novelty_base: dlplan.NoveltyBase
    # Initialized before iteration
    instance_information: InstanceInformation
    state_space: dlplan.StateSpace = None
    goal_distance_information: dlplan.GoalDistanceInformation = None
    state_information: dlplan.StateInformation = None
    tuple_graphs: List[dlplan.TupleGraph] = None
    initial_s_idxs: List[int] = None  # in cases we need multiple initial states
    # Initialized in every iteration
    iteration_information = IterationInformation = None
    feature_valuations: List[FeatureValuation] = None
    state_equivalence: InstanceStateEquivalence = None
    state_pair_equivalence: InstanceStatePairEquivalence = None
    tuple_graph_equivalences: List[TupleGraphEquivalence] = None

    def set_state_space(self, state_space: dlplan.StateSpace):
        """ Set state space and writes it to a file. """
        self.state_space = state_space
        write_file(self.instance_information.workspace / f"{self.instance_information.name}.dot", state_space.to_dot(1))

    def set_goal_distance_information(self, goal_distance_information: dlplan.GoalDistanceInformation):
        self.goal_distance_information =  goal_distance_information

    def set_state_information(self, state_information: dlplan.StateInformation):
        self.state_information = state_information

    def set_tuple_graphs(self, tuple_graphs: List[dlplan.TupleGraph]):
        """ Set tuple graphs and writes them to files. """
        self.tuple_graphs = tuple_graphs
        for tuple_graph in tuple_graphs.values():
            write_file(self.instance_information.tuple_graph_workspace / f"{tuple_graph.get_root_state_index()}.dot", tuple_graph.to_dot(1))

    def set_iteration_information(self, iteration_information: IterationInformation):
        self.iteration_information = iteration_information
        write_file(self.iteration_information.workspace / f"{self.instance_information.name}.dot", self.state_space.to_dot(1))
        for tuple_graph in self.tuple_graphs.values():
            write_file(self.iteration_information.tuple_graph_workspace / f"{tuple_graph.get_root_state_index()}.dot", tuple_graph.to_dot(1))

    def set_feature_valuations(self, feature_valuations: List[FeatureValuation]):
        """ Set feature valuations and writes them to files. """
        self.feature_valuations = feature_valuations
        write_file(self.iteration_information.feature_valuations_workspace / "feature_valuations.txt", str(self.feature_valuations))

    def set_state_equivalence(self, state_equivalence: InstanceStateEquivalence):
        """ Set state equivalence and writes it to files. """
        self.state_equivalence = state_equivalence
        write_file(self.iteration_information.state_equivalence_workspace / "state_equivalence.txt", str(self.state_equivalence))

    def set_state_pair_equivalence(self, state_pair_equivalence: InstanceStatePairEquivalence):
        """ Set state pair equivalence and writes it to files. """
        self.state_pair_equivalence = state_pair_equivalence
        write_file(self.iteration_information.state_pair_equivalence_workspace / "state_pair_equivalence.txt", str(self.state_pair_equivalence))

    def set_tuple_graph_equivalences(self, tuple_graph_equivalences: List[TupleGraphEquivalence]):
        """ Set tuple graph equivalences and writes them to files. """
        self.tuple_graph_equivalences = tuple_graph_equivalences
        write_file(self.iteration_information.tuple_graph_equivalences_workspace / "tuple_graph_equivalences.txt", str(self.tuple_graph_equivalences))


