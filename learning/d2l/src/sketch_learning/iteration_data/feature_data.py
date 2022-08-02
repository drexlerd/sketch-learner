import logging
import dlplan

from typing import Dict, List, MutableSet, Tuple
from dataclasses import dataclass, field

from ..instance_data.instance_data import InstanceData
from ..domain_data.domain_data import DomainData


@dataclass
class DomainFeatureData:
    boolean_features: List[dlplan.Boolean]
    numerical_features: List[dlplan.Numerical]

    def print(self):
        print("Domain feature data:")
        print(f"    Boolean features: {self.boolean_features}")
        print(f"    Numerical features: {self.numerical_features}")


@dataclass
class InstanceFeatureData:
    boolean_feature_valuations: Dict[int, List[bool]]
    numerical_feature_valuations: Dict[int, List[int]]

    def print(self):
        print("Instance feature data:")
        print(f"    Boolean feature valuations: {self.boolean_feature_valuations}")
        print(f"    Numerical feature valuations: {self.numerical_feature_valuations}")


class FeatureDataFactory:
    def generate_feature_data(self, config, domain_data: DomainData, instance_datas: List[InstanceData]) -> Tuple[DomainFeatureData, List[InstanceFeatureData]]:
        assert instance_datas
        boolean_features, numerical_features = self._generate_features(config, domain_data, instance_datas)
        domain_feature_data = DomainFeatureData(boolean_features, numerical_features)
        instance_feature_datas = [self._evaluate_features(boolean_features, numerical_features, instance_data) for instance_data in instance_datas]
        return domain_feature_data, instance_feature_datas

    def _generate_features(self, config, domain_data: DomainData, instance_datas: List[InstanceData]) -> Tuple[List[dlplan.Boolean], List[dlplan.Numerical]]:
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
            dlplan_states = []
            for instance_data in instance_datas:
                dlplan_states.extend(instance_data.transition_system.states_by_index)
            feature_reprs = feature_generator.generate(syntactic_element_factory, config.complexity, config.time_limit, config.feature_limit, config.num_threads_feature_generator, dlplan_states)
            numerical_features = [syntactic_element_factory.parse_numerical(repr) for repr in feature_reprs if repr.startswith("n_")]
            boolean_features = [syntactic_element_factory.parse_boolean(repr) for repr in feature_reprs if repr.startswith("b_")]
        return boolean_features, numerical_features

    def _evaluate_features(self, boolean_features: List[dlplan.Boolean], numerical_features: List[dlplan.Numerical], instance_data: InstanceData) -> InstanceFeatureData:
        # boolean_feature_valuations[s][b] is feature valuation of b-th boolean, s-th state
        boolean_feature_valuations = dict()
        numerical_feature_valuations = dict()
        for s_idx, dlplan_state in enumerate(instance_data.transition_system.states_by_index):
            b_per_state = []
            for boolean_feature in boolean_features:
                b_per_state.append(boolean_feature.evaluate(dlplan_state))
            boolean_feature_valuations[s_idx] = b_per_state
            n_per_state = []
            for numerical_feature in numerical_features:
                n_per_state.append(numerical_feature.evaluate(dlplan_state))
            numerical_feature_valuations[s_idx] = n_per_state
        for s_idx, state in enumerate(instance_data.transition_system.states_by_index):
            print(s_idx, str(state), numerical_feature_valuations[s_idx])
        return InstanceFeatureData(boolean_feature_valuations, numerical_feature_valuations)