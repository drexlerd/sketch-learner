from dataclasses import dataclass
from typing import List, Dict, Union

import pymimir as mm
import dlplan.policy as dlplan_policy

from .feature_pool import Feature
from .state_pair_equivalence import StatePairEquivalence
from .tuple_graph_equivalence import TupleGraphEquivalence

from ..preprocessing import InstanceData


@dataclass
class IterationData:
    """ Store data that is being computed in each iteration of learning sketches. """
    # Changes in each iterations
    instance_datas: List[InstanceData] = None

    gfa_states: List[mm.GlobalFaithfulAbstractState] = None

    feature_pool: List[Feature] = None
    gfa_state_global_idx_to_feature_evaluations: Dict[int, List[Union[bool, int]]] = None

    state_pair_equivalences: List[dlplan_policy.Rule] = None
    gfa_state_global_idx_to_state_pair_equivalence: Dict[int, StatePairEquivalence] = None

    gfa_state_global_idx_to_tuple_graph_equivalence: Dict[int, TupleGraphEquivalence] = None
