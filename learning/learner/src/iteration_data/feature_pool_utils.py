from typing import  List

from dlplan.generator import FeatureGenerator

from .feature_pool import Feature, FeaturePool

from ..domain_data.domain_data import DomainData
from ..instance_data.instance_data import InstanceData


def compute_feature_pool(config, domain_data: DomainData, instance_datas: List[InstanceData]):
    dlplan_states = set()
    for instance_data in instance_datas:
        dlplan_states.update(set(instance_data.state_space.get_states().values()))
    dlplan_states = list(dlplan_states)

    syntactic_element_factory = domain_data.syntactic_element_factory
    feature_generator = FeatureGenerator()
    feature_generator.set_generate_inclusion_boolean(False)
    feature_generator.set_generate_diff_concept(False)
    feature_generator.set_generate_or_concept(False)
    feature_generator.set_generate_projection_concept(False)
    feature_generator.set_generate_subset_concept(False)
    feature_generator.set_generate_compose_role(False)
    feature_generator.set_generate_diff_role(False)
    feature_generator.set_generate_identity_role(False)
    feature_generator.set_generate_not_role(False)
    feature_generator.set_generate_or_role(False)
    feature_generator.set_generate_top_role(False)
    feature_generator.set_generate_transitive_reflexive_closure_role(False)
    features = []
    if config.generate_features:
        [generated_booleans, generated_numericals, _, _] = feature_generator.generate(syntactic_element_factory, dlplan_states, config.concept_complexity_limit, config.role_complexity_limit, config.boolean_complexity_limit, config.count_numerical_complexity_limit, config.distance_numerical_complexity_limit, config.time_limit, config.feature_limit)
        for boolean in generated_booleans:
            features.append(Feature(boolean, boolean.compute_complexity() + 1 + 1))
        for numerical in generated_numericals:
            features.append(Feature(numerical, numerical.compute_complexity() + 1))
    for boolean in config.add_boolean_features:
        boolean = syntactic_element_factory.parse_boolean(boolean)
        features.append(Feature(boolean, boolean.compute_complexity() + 1 + 1))
    for numerical in config.add_numerical_features:
        numerical = syntactic_element_factory.parse_numerical(numerical)
        features.append(Feature(numerical, numerical.compute_complexity() + 1))
    return FeaturePool(features)