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

    def print_statistics(self):
        pass

