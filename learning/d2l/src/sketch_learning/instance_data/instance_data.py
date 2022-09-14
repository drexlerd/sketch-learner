import dlplan
from dataclasses import dataclass
from typing import List

from ..domain_data.domain_data import DomainData
from .tuple_graph import TupleGraph
from .state_pair_classifier import StatePairClassifier
from ..iteration_data.instance_feature_data import InstanceFeatureData
from ..iteration_data.state_pair_equivalence import StatePairEquivalence
from ..iteration_data.tuple_graph_equivalence import TupleGraphEquivalence
from ..driver import Bunch


@dataclass
class InstanceData:
    """ """
    id: int
    instance_information: Bunch
    domain_data: DomainData
    state_space: dlplan.StateSpace
    goal_distance_information: dlplan.GoalDistanceInformation = None
    state_information: dlplan.StateInformation = None
    tuple_graphs: List[TupleGraph] = None
    state_pair_classifier: StatePairClassifier = None
    instance_feature_data: InstanceFeatureData = None
    state_pair_equivalence: StatePairEquivalence = None
    tuple_graph_equivalences: List[TupleGraphEquivalence] = None

    def print_statistics(self):
        pass
