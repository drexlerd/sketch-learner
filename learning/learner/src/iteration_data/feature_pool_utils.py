from typing import  List

from dlplan.core import Boolean, Numerical
from dlplan.generator import FeatureGenerator

from learner.src.domain_data.domain_data import DomainData
from learner.src.instance_data.instance_data import InstanceData
from learner.src.iteration_data.feature_pool import Feature, FeaturePool


def add_boolean_feature(feature_pool: FeaturePool, boolean: Boolean):
    feature_pool.boolean_features.add_feature(Feature(boolean, boolean.compute_complexity() + 1 + 1))


def add_numerical_feature(feature_pool: FeaturePool, numerical: Numerical):
    feature_pool.numerical_features.add_feature(Feature(numerical, numerical.compute_complexity() + 1))


def compute_feature_pool(config, domain_data: DomainData, instance_datas: List[InstanceData]):
    dlplan_states = set()
    for instance_data in instance_datas:
        dlplan_states.update(set(instance_data.state_space.get_states().values()))
    dlplan_states = list(dlplan_states)

    syntactic_element_factory = domain_data.syntactic_element_factory
    feature_pool = FeaturePool()
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
    if config.generate_features:
        [generated_booleans, generated_numericals, _, _] = feature_generator.generate(syntactic_element_factory, dlplan_states, config.concept_complexity_limit, config.role_complexity_limit, config.boolean_complexity_limit, config.count_numerical_complexity_limit, config.distance_numerical_complexity_limit, config.time_limit, config.feature_limit)
        for boolean in generated_booleans:
            add_boolean_feature(feature_pool, boolean)
        for numerical in generated_numericals:
            add_numerical_feature(feature_pool, numerical)
    for boolean in config.add_boolean_features:
        add_boolean_feature(feature_pool, syntactic_element_factory.parse_boolean(boolean))
    for numerical in config.add_numerical_features:
        add_numerical_feature(feature_pool, syntactic_element_factory.parse_numerical(numerical))
    return feature_pool