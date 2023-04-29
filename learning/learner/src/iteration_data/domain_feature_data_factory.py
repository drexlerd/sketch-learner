import logging
import dlplan

from dataclasses import dataclass
from typing import  List, Tuple

from .domain_feature_data import DomainFeatureData, Feature

from ..domain_data.domain_data import DomainData
from ..instance_data.instance_data import InstanceData


@dataclass
class DomainFeatureDataStatistics:
    num_dlplan_states: int = 0
    num_boolean_features: int = 0
    num_numerical_features: int = 0

    def increase_num_dlplan_states(self, num):
        self.num_dlplan_states += num

    def increase_num_boolean_features(self, num: int):
        self.num_boolean_features += num

    def increase_num_numerical_features(self, num: int):
        self.num_numerical_features += num

    def print(self):
        print("DomainFeatureDataStatistics:")
        print("    num_dlplan_states:", self.num_dlplan_states)
        print("    num_boolean_features:", self.num_boolean_features)
        print("    num_numerical_features:", self.num_numerical_features)


class DomainFeatureDataFactory:
    def __init__(self):
        self.statistics = DomainFeatureDataStatistics()

    def make_domain_feature_data_from_instance_datas(self, config, domain_data: DomainData, instance_datas: List[InstanceData]):
        dlplan_states = set()
        for instance_data in instance_datas:
            dlplan_states.update(instance_data.state_space.get_states())
        return self.make_domain_feature_data(config, domain_data, list(dlplan_states))

    def make_domain_feature_data(self, config, domain_data: DomainData, dlplan_states: List[dlplan.State]):
        boolean_features, numerical_features = self._generate_features(config, domain_data, dlplan_states)
        self.statistics.increase_num_dlplan_states(len(dlplan_states))
        self.statistics.increase_num_boolean_features(len(boolean_features))
        self.statistics.increase_num_numerical_features(len(numerical_features))
        domain_feature_data = DomainFeatureData()
        for boolean_feature in boolean_features:
            domain_feature_data.boolean_features.add_feature(Feature(boolean_feature, boolean_feature.compute_complexity() + 1))
        for numerical_feature in numerical_features:
            domain_feature_data.numerical_features.add_feature(Feature(numerical_feature, numerical_feature.compute_complexity() + 1))
        for zero_cost_boolean_feature in domain_data.zero_cost_boolean_features.features_by_index:
            domain_feature_data.boolean_features.add_feature(zero_cost_boolean_feature)
        for zero_cost_numerical_feature in domain_data.zero_cost_numerical_features.features_by_index:
            domain_feature_data.numerical_features.add_feature(zero_cost_numerical_feature)
        return domain_feature_data

    def _generate_features(self, config, domain_data: DomainData, dlplan_states: List[dlplan.State]) -> Tuple[List[dlplan.Boolean], List[dlplan.Numerical]]:
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
            feature_reprs = feature_generator.generate(syntactic_element_factory, config.concept_complexity_limit, config.role_complexity_limit, config.boolean_complexity_limit, config.count_numerical_complexity_limit, config.distance_numerical_complexity_limit, config.time_limit, config.feature_limit, config.num_threads_feature_generator, dlplan_states)
            numerical_features = [syntactic_element_factory.parse_numerical(repr) for repr in feature_reprs if repr.startswith("n_")]
            boolean_features = [syntactic_element_factory.parse_boolean(repr) for repr in feature_reprs if repr.startswith("b_")]
        return boolean_features, numerical_features
