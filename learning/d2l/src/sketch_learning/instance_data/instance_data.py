import dlplan
from dataclasses import dataclass

from .transition_system import TransitionSystem
from ..domain_data.domain_data import DomainData
from ..driver import Bunch


@dataclass
class InstanceData:
    """ """
    id: int
    instance_information: Bunch
    domain_data: DomainData
    transition_system: TransitionSystem
    instance_info: dlplan.InstanceInfo

    def print_statistics(self):
        pass
