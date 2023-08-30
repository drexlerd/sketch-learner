from dlplan.core import VocabularyInfo, SyntacticElementFactory
from dlplan.generator import FeatureGenerator
from dlplan.policy import PolicyBuilder

from dataclasses import dataclass

from learner.src.iteration_data.state_pair_equivalence import StatePairEquivalenceClasses
from learner.src.iteration_data.feature_pool import FeaturePool


@dataclass
class DomainData:
    """ Store data related to a domain. """
    domain_filename: str
    vocabulary_info: VocabularyInfo
    policy_builder: PolicyBuilder
    syntactic_element_factory: SyntacticElementFactory
    feature_generator: FeatureGenerator
    domain_feature_data: FeaturePool = None
    domain_state_pair_equivalence: StatePairEquivalenceClasses = None
