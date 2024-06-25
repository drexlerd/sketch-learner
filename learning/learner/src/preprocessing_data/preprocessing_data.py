from dataclasses import dataclass
from typing import Dict, List

import pymimir as mm

from ..domain_data.domain_data import DomainData
from ..instance_data.instance_data import InstanceData
from .state_finder import StateFinder

@dataclass
class PreprocessingData:
    """ Immutable data class. """
    _domain_data: DomainData
    _instance_datas: List[InstanceData]
    _state_finder: StateFinder
    _gfa_states_by_id: Dict[int, mm.GlobalFaithfulAbstractState]
    _gfa_state_id_to_tuple_graph: Dict[int, mm.TupleGraph]

    @property
    def domain_data(self):
        return self._domain_data

    @property
    def instance_datas(self):
        return self._instance_datas

    @property
    def state_finder(self):
        return self._state_finder

    @property
    def gfa_states_by_id(self):
        return self._gfa_states_by_id

    @property
    def gfa_state_id_to_tuple_graph(self):
        return self._gfa_state_id_to_tuple_graph
