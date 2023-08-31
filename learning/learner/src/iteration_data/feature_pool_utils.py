from typing import  List

from dlplan.core import SyntacticElementFactory
from dlplan.generator import FeatureGenerator

from learner.src.domain_data.domain_data import DomainData
from learner.src.instance_data.instance_data import InstanceData
from learner.src.iteration_data.feature_pool import Feature, FeaturePool


def add_features(syntactic_element_factory: SyntacticElementFactory, feature_reprs: List[str], feature_pool: FeaturePool):
    for feature_repr in feature_reprs:
        # To use features from parent node for free have add them with cost 1 and add cost + 1 to each generated feature
        # To break ties in favor of numerical features, we add an additional + 1 to the complexity of Boolean features.
        if feature_repr.startswith("n_"):
            numerical = syntactic_element_factory.parse_numerical(feature_repr)
            feature_pool.numerical_features.add_feature(Feature(numerical, numerical.compute_complexity() + 1))
        elif feature_repr.startswith("b_"):
            boolean = syntactic_element_factory.parse_boolean(feature_repr)
            feature_pool.boolean_features.add_feature(Feature(boolean, boolean.compute_complexity() + 1 + 1))


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
        feature_reprs = feature_generator.generate(syntactic_element_factory, dlplan_states, config.concept_complexity_limit, config.role_complexity_limit, config.boolean_complexity_limit, config.count_numerical_complexity_limit, config.distance_numerical_complexity_limit, config.time_limit, config.feature_limit)
        add_features(domain_data.syntactic_element_factory, feature_reprs, feature_pool)
    if config.add_features:
        add_features(domain_data.syntactic_element_factory, config.add_features, feature_pool)
    return feature_pool