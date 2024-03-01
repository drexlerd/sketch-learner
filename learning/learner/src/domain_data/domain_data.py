from dataclasses import dataclass

from dlplan.core import VocabularyInfo, SyntacticElementFactory
from dlplan.policy import PolicyFactory

from learner.src.iteration_data.state_pair_equivalence import PerStateStatePairEquivalences
from learner.src.iteration_data.feature_pool import FeaturePool


@dataclass
class DomainData:
    """ Store data related to a domain. """
    domain_filename: str
    vocabulary_info: VocabularyInfo
    policy_builder: PolicyFactory
    syntactic_element_factory: SyntacticElementFactory
    domain_feature_data: FeaturePool = None
    domain_state_pair_equivalence: PerStateStatePairEquivalences = None
