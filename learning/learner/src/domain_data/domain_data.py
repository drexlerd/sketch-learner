from dlplan.core import VocabularyInfo, SyntacticElementFactory
from dlplan.generator import FeatureGenerator
from dlplan.policy import PolicyBuilder

from dataclasses import dataclass

from learner.src.iteration_data.state_pair_equivalence import DomainStatePairEquivalence
from learner.src.iteration_data.domain_feature_data import DomainFeatureData


@dataclass
class DomainData:
    """ Store data related to a domain. """
    domain_filename: str
    vocabulary_info: VocabularyInfo
    policy_builder: PolicyBuilder
    syntactic_element_factory: SyntacticElementFactory
    feature_generator: FeatureGenerator
    domain_feature_data: DomainFeatureData = None
    domain_state_pair_equivalence: DomainStatePairEquivalence = None
    # store all generated features to not let them run out of scope and to keep cache entries alive
    all_domain_feature_data: DomainFeatureData = DomainFeatureData()
