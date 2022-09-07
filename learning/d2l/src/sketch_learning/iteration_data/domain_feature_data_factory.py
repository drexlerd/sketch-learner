import logging
import dlplan

from dataclasses import dataclass
from typing import  List, Tuple

from .domain_feature_data import DomainFeatureData

from ..domain_data.domain_data import DomainData
from ..instance_data.instance_data import InstanceData
from ..instance_data.state_pair_classifier import StatePairClassifier


@dataclass
class DomainFeatureDataStatistics:
    num_dlplan_state_pairs: int = 0
    num_boolean_features: int = 0
    num_numerical_features: int = 0

    def increase_num_dlplan_state_pairs(self, num):
        self.num_dlplan_state_pairs += num

    def increase_num_boolean_features(self, num: int):
        self.num_boolean_features += num

    def increase_num_numerical_features(self, num: int):
        self.num_numerical_features += num

    def print(self):
        print("Number of dlplan state pairs:", self.num_dlplan_state_pairs)
        print("Number of boolean features:", self.num_boolean_features)
        print("Number of numerical features:", self.num_numerical_features)


class DomainFeatureDataFactory:
    def __init__(self):
        self.statistics = DomainFeatureDataStatistics()

    def make_domain_feature_data_from_subproblems(self, config, domain_data: DomainData, instance_datas: List[InstanceData], state_pair_classifiers_by_instance: List[StatePairClassifier]):
        dlplan_states = set()
        for instance_data, state_pair_classifier in zip(instance_datas, state_pair_classifiers_by_instance):
            dlplan_states.update([dlplan_state for dlplan_state in instance_data.transition_system.s_idx_to_dlplan_state.values()])
        return self.make_domain_feature_data(config, domain_data, list(dlplan_states))

    def make_domain_feature_data_from_instances(self, config, domain_data: DomainData, instance_datas: List[InstanceData]):
        dlplan_state_pairs = []
        for selected_instance_data in instance_datas:
            dlplan_state_pairs.extend([(selected_instance_data.transition_system.s_idx_to_dlplan_state[0], dlplan_state) for dlplan_state in selected_instance_data.transition_system.s_idx_to_dlplan_state.values()])
        return self.make_domain_feature_data(config, domain_data, dlplan_state_pairs)

    def make_domain_feature_data(self, config, domain_data: DomainData, dlplan_state_pairs: List[Tuple[dlplan.State, dlplan.State]]):
        boolean_features, numerical_features = self._generate_features(config, domain_data, dlplan_state_pairs)
        self.statistics.increase_num_dlplan_state_pairs(len(dlplan_state_pairs))
        self.statistics.increase_num_boolean_features(len(boolean_features))
        self.statistics.increase_num_numerical_features(len(numerical_features))
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
