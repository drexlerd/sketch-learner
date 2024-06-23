from dataclasses import dataclass
from typing import List, Dict, Union

import pymimir as mm

from dlplan.core import VocabularyInfo, SyntacticElementFactory
from dlplan.policy import PolicyFactory

from ..iteration_data.state_pair_equivalence import StatePairEquivalenceClasses
from ..iteration_data.feature_pool import FeaturePool


@dataclass
class DomainData:
    """ Store data related to a domain. """

    # Persistant data.
    domain_filename: str
    vocabulary_info: VocabularyInfo
    policy_builder: PolicyFactory
    syntactic_element_factory: SyntacticElementFactory
    instance_idx_remap : List[int] = None
    gfa_state_id_to_tuple_graph : Dict[int, mm.TupleGraph] = None

    # Changes in each iterations
    gfa_states: List[mm.GlobalFaithfulAbstractState] = None
    feature_pool: FeaturePool = None
    gfa_state_id_to_feature_evaluations: Dict[int, List[Union[bool, int]]] = None
    domain_state_pair_equivalence: StatePairEquivalenceClasses = None
