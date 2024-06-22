from dataclasses import dataclass
from typing import List

from dlplan.core import VocabularyInfo, SyntacticElementFactory
from dlplan.policy import PolicyFactory

from ..iteration_data.state_pair_equivalence import StatePairEquivalenceClasses
from ..iteration_data.feature_pool import FeaturePool


@dataclass
class DomainData:
    """ Store data related to a domain. """
    domain_filename: str
    vocabulary_info: VocabularyInfo
    policy_builder: PolicyFactory
    syntactic_element_factory: SyntacticElementFactory
    instance_idx_remap : List[int] = None
    feature_pool: FeaturePool = None
    domain_state_pair_equivalence: StatePairEquivalenceClasses = None
