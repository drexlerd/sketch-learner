import logging
import dlplan

from dataclasses import dataclass
from typing import  List, Tuple

from learner.src.domain_data.domain_data import DomainData
from learner.src.instance_data.instance_data import InstanceData
from learner.src.iteration_data.domain_feature_data import DomainFeatureData, Feature


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
            dlplan_states.update(set(instance_data.state_space.get_states().values()))
        self.make_domain_feature_data(config, domain_data, list(dlplan_states))

    def make_domain_feature_data(self, config, domain_data: DomainData, dlplan_states: List[dlplan.State]):
        boolean_features, numerical_features = self._generate_features(config, domain_data, dlplan_states)
        self.statistics.increase_num_dlplan_states(len(dlplan_states))
        self.statistics.increase_num_boolean_features(len(boolean_features))
        self.statistics.increase_num_numerical_features(len(numerical_features))
        domain_feature_data = DomainFeatureData()
        # To use features from parent node for free have add them with cost 1 and add cost + 1 to each generated feature
        for boolean_feature in boolean_features:
            # To break ties in favor of numerical features, we add an additional + 1 to the complexity of Boolean features.
            domain_feature_data.boolean_features.add_feature(Feature(boolean_feature, boolean_feature.compute_complexity() + 1 + 1))
            domain_data.all_domain_feature_data.boolean_features.add_feature(Feature(boolean_feature, boolean_feature.compute_complexity() + 1 + 1))
        for numerical_feature in numerical_features:
            domain_feature_data.numerical_features.add_feature(Feature(numerical_feature, numerical_feature.compute_complexity() + 1))
            domain_data.all_domain_feature_data.numerical_features.add_feature(Feature(numerical_feature, numerical_feature.compute_complexity() + 1))
        domain_data.domain_feature_data = domain_feature_data

    def _generate_features(self, config, domain_data: DomainData, dlplan_states: List[dlplan.State]) -> Tuple[List[dlplan.Boolean], List[dlplan.Numerical]]:
        """ Generate features and their evaluations
        for all states in the given transition systems. """
        syntactic_element_factory = domain_data.syntactic_element_factory
        numerical_features = []
        boolean_features = []
        if config.generate_features:
            feature_generator = domain_data.feature_generator
            feature_reprs = feature_generator.generate(syntactic_element_factory, dlplan_states, config.concept_complexity_limit, config.role_complexity_limit, config.boolean_complexity_limit, config.count_numerical_complexity_limit, config.distance_numerical_complexity_limit, config.time_limit, config.feature_limit)
            numerical_features.extend([syntactic_element_factory.parse_numerical(repr) for repr in feature_reprs if repr.startswith("n_")])
            boolean_features.extend([syntactic_element_factory.parse_boolean(repr) for repr in feature_reprs if repr.startswith("b_")])
        if config.add_features:
            numerical_features.extend([syntactic_element_factory.parse_numerical(repr) for repr in config.add_features if repr.startswith("n_")])
            boolean_features.extend([syntactic_element_factory.parse_boolean(repr) for repr in config.add_features if repr.startswith("b_")])
        return boolean_features, numerical_features
