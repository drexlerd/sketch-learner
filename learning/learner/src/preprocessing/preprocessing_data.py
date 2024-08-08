from dataclasses import dataclass
from typing import Dict, List

import pymimir as mm

from .domain_data import DomainData
from .instance_data import InstanceData


@dataclass
class PreprocessingData:
    """ Immutable data class. """
    _domain_data: DomainData
    _instance_datas: List[InstanceData]
    _ss_state_idx_to_tuple_graph: List[Dict[int, mm.TupleGraph]]

    @property
    def domain_data(self):
        return self._domain_data

    @property
    def instance_datas(self):
        return self._instance_datas

    @property
    def ss_state_idx_to_tuple_graph(self):
        return self._ss_state_idx_to_tuple_graph
