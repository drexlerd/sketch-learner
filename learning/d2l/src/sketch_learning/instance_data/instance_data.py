import dlplan
from dataclasses import dataclass

from ..domain_data.domain_data import DomainData
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

    def print_statistics(self):
        pass
