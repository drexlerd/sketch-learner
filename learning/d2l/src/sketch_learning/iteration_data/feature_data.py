import logging
import dlplan

from typing import Dict, List, MutableSet, Tuple
from dataclasses import dataclass, field

from ..domain_data.domain_data import DomainData
from ..instance_data.instance_data import InstanceData


@dataclass
class FeatureData:
    boolean_features: List[dlplan.Boolean]
    numerical_features: List[dlplan.Numerical]
    boolean_feature_valuations: List[List[List[bool]]]
    numerical_feature_valuations: List[List[List[int]]]


class FeatureDataFactory:
    def generate_feature_data(self, config, domain_data : DomainData, instance_datas : List[InstanceData]) -> FeatureData:
        boolean_features, numerical_features = self._generate_features(config, domain_data, instance_datas)
        boolean_feature_valuations, numerical_feature_valuations = self._evaluate_features(boolean_features, numerical_features, instance_datas)
        return FeatureData(boolean_features, numerical_features, boolean_feature_valuations, numerical_feature_valuations)

    def _generate_features(self, config, domain_data : DomainData, instance_datas : List[InstanceData]) -> Tuple[List[dlplan.Boolean], List[dlplan.Numerical]]:
        """ Generate features and their evaluations
        for all states in the given transition systems. """
        # Generate the features
        syntactic_element_factory = domain_data.syntactic_element_factory
        # TODO: We might want to store features in same list for easier indexing.
        if config.debug_features:
            logging.info("Using predefined features:")
            # Use custom features
            numerical_features = [syntactic_element_factory.parse_numerical(repr) for repr in config.debug_features if repr.startswith("n_")]
            boolean_features = [syntactic_element_factory.parse_boolean(repr) for repr in config.debug_features if repr.startswith("b_")]
        else:
            # Generate features
            feature_generator = domain_data.feature_generator
            dlplan_states = [dlplan_state for instance_data in instance_datas for dlplan_state in instance_data.transition_system.states_by_index]
            feature_reprs = feature_generator.generate(syntactic_element_factory, config.complexity, config.time_limit, config.feature_limit, config.num_threads_feature_generator, dlplan_states)
            numerical_features = [syntactic_element_factory.parse_numerical(repr) for repr in feature_reprs if repr.startswith("n_")]
            boolean_features = [syntactic_element_factory.parse_boolean(repr) for repr in feature_reprs if repr.startswith("b_")]
        return boolean_features, numerical_features


    def _evaluate_features(self, boolean_features : List[dlplan.Boolean], numerical_features : List[dlplan.Numerical], instance_datas : List[InstanceData]):
        # boolean_feature_valuations[i][s][b] is feature valuation of b-th boolean, s-th state, i-th instance_data
        boolean_feature_valuations = []
        numerical_feature_valuations = []
        for instance_data in instance_datas:
            b_per_instance = []
            n_per_instance = []
            for dlplan_state in instance_data.transition_system.states_by_index:
                b_per_state = []
                for boolean_feature in boolean_features:
                    b_per_state.append(boolean_feature.evaluate(dlplan_state))
                b_per_instance.append(b_per_state)
                n_per_state = []
                for numerical_feature in numerical_features:
                    n_per_state.append(numerical_feature.evaluate(dlplan_state))
                n_per_instance.append(n_per_state)
            boolean_feature_valuations.append(b_per_instance)
            numerical_feature_valuations.append(n_per_instance)
        return boolean_feature_valuations, numerical_feature_valuations
