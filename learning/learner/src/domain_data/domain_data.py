import dlplan

from dataclasses import dataclass

from learner.src.iteration_data.state_pair_equivalence import DomainStatePairEquivalence
from learner.src.iteration_data.domain_feature_data import DomainFeatureData


@dataclass
class DomainData:
    """ Store data related to a domain. """
    domain_filename: str
    vocabulary_info: dlplan.VocabularyInfo
    policy_builder: dlplan.PolicyBuilder
    syntactic_element_factory: dlplan.SyntacticElementFactory
    feature_generator: dlplan.FeatureGenerator
    domain_feature_data: DomainFeatureData = None
    domain_state_pair_equivalence: DomainStatePairEquivalence = None
    # store all generated features to not let them run out of scope and to keep cache entries alive
    all_domain_feature_data: DomainFeatureData = DomainFeatureData()
