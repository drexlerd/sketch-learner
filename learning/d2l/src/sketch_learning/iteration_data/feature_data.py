import logging
import dlplan

from abc import ABC, abstractmethod
from typing import Dict, List, MutableSet, Tuple
from dataclasses import dataclass, field

from .sketch import Sketch

from ..instance_data.instance_data import InstanceData
from ..domain_data.domain_data import DomainData


@dataclass
class DomainFeatureData:
    """ DomainFeatureData stores all novel Boolean and Numerical features for a set of dlplan states. """
    boolean_features: List[dlplan.Boolean]
    numerical_features: List[dlplan.Numerical]

    def print(self):
        print("Domain feature data:")
        print(f"    Boolean features: {self.boolean_features}")
        print(f"    Numerical features: {self.numerical_features}")


@dataclass
class InstanceFeatureData:
    """ InstanceFeatureData stores feature valuations for each state in an instance. """
    boolean_feature_valuations: Dict[int, List[bool]]
    numerical_feature_valuations: Dict[int, List[int]]

    def print(self):
        print("Instance feature data:")
        print(f"    Boolean feature valuations: {self.boolean_feature_valuations}")
        print(f"    Numerical feature valuations: {self.numerical_feature_valuations}")


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


class InstanceFeatureDataFactory:
    def make_instance_feature_datas(self, instance_datas: List[InstanceData], domain_feature_data: DomainFeatureData) -> Tuple[DomainFeatureData, List[InstanceFeatureData]]:
        instance_feature_datas = [self._evaluate_features(instance_data, domain_feature_data) for instance_data in instance_datas]
        return instance_feature_datas

    def _evaluate_features(self, instance_data: InstanceData, domain_feature_data: DomainFeatureData) -> InstanceFeatureData:
        # boolean_feature_valuations[s][b] is feature valuation of b-th boolean, s-th state
        boolean_feature_valuations = dict()
        numerical_feature_valuations = dict()
        for s_idx, dlplan_state in enumerate(instance_data.transition_system.states_by_index):
            b_per_state = []
            for boolean_feature in domain_feature_data.boolean_features:
                b_per_state.append(boolean_feature.evaluate(dlplan_state))
            boolean_feature_valuations[s_idx] = b_per_state
            n_per_state = []
            for numerical_feature in domain_feature_data.numerical_features:
                n_per_state.append(numerical_feature.evaluate(dlplan_state))
            numerical_feature_valuations[s_idx] = n_per_state
        return InstanceFeatureData(boolean_feature_valuations, numerical_feature_valuations)


@dataclass
class SketchFeatureData:
    """ SketchFeatureData stores seed features based on effects of sketch. """
    boolean_features: List[dlplan.Boolean]
    numerical_features: List[dlplan.Numerical]

    def print(self):
        print("Sketch feature data:")
        print(f"    Boolean features: {self.boolean_features}")
        print(f"    Numerical features: {self.numerical_features}")

class SketchFeatureDataFactory:
    def make_sketch_feature_data(self, sketch: Sketch):
        return SketchFeatureData(sketch.dlplan_policy.get_boolean_features(), sketch.dlplan_policy.get_numerical_features())
