import logging
import dlplan
import tarski

from dataclasses import dataclass

from ..iteration_data.domain_feature_data import Features


@dataclass
class DomainData:
    """ Store data related to a domain. """
    domain_filename: str
    vocabulary_info: dlplan.VocabularyInfo
    syntactic_element_factory: dlplan.SyntacticElementFactory
    feature_generator: dlplan.FeatureGenerator
    zero_cost_boolean_features = Features()
    zero_cost_numerical_features = Features()
