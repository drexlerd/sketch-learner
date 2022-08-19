import logging
import dlplan

from typing import  List,  Tuple

from .domain_feature_data import DomainFeatureData

from ..domain_data.domain_data import DomainData


class DomainFeatureDataFactory:
    def make_domain_feature_data(self, config, domain_data: DomainData, dlplan_state_pairs: List[Tuple[dlplan.State, dlplan.State]]):
        boolean_features, numerical_features = self._generate_features(config, domain_data, dlplan_state_pairs)
        return DomainFeatureData(boolean_features, numerical_features)

    def _generate_features(self, config, domain_data: DomainData, dlplan_state_pairs: List[Tuple[dlplan.State, dlplan.State]]) -> Tuple[List[dlplan.Boolean], List[dlplan.Numerical]]:
        """ Generate features and their evaluations
        for all states in the given transition systems. """
        syntactic_element_factory = domain_data.syntactic_element_factory
        if config.debug_features:
            logging.info("Using predefined features:")
            # Use custom features
            numerical_features = [syntactic_element_factory.parse_numerical(repr) for repr in config.debug_features if repr.startswith("n_")]
            boolean_features = [syntactic_element_factory.parse_boolean(repr) for repr in config.debug_features if repr.startswith("b_")]
        else:
            # Generate features
            feature_generator = domain_data.feature_generator
            feature_reprs = feature_generator.generate(syntactic_element_factory, config.complexity, config.time_limit, config.feature_limit, config.num_threads_feature_generator, dlplan_state_pairs)
            numerical_features = [syntactic_element_factory.parse_numerical(repr) for repr in feature_reprs if repr.startswith("n_")]
            boolean_features = [syntactic_element_factory.parse_boolean(repr) for repr in feature_reprs if repr.startswith("b_")]
        return boolean_features, numerical_features
