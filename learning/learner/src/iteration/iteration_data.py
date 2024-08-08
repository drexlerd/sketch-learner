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

    feature_pool: List[Feature] = None
    instance_idx_to_ss_idx_to_feature_valuations: Dict[int, List[List[Union[bool, int]]]] = None

    state_pair_equivalences: List[dlplan_policy.Rule] = None
    instance_idx_to_ss_idx_to_state_pair_equivalence: Dict[int, Dict[int, StatePairEquivalence]] = None

    instance_idx_to_ss_idx_to_tuple_graph_equivalence: Dict[int, Dict[int, TupleGraphEquivalence]] = None
