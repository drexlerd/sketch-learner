from enum import Enum
from typing import List, Dict

import pymimir as mm
import dlplan.generator as dlplan_generator

from .feature_pool import Feature
from .iteration_data import IterationData

from ..preprocessing import PreprocessingData, StateFinder


class FeatureChange(Enum):
    UP = 0
    DOWN = 1
    BOT = 2


def compute_feature_pool(preprocessing_data: PreprocessingData,
                         iteration_data: IterationData,
                         disable_feature_generation: bool,
                         concept_complexity_limit: int,
                         role_complexity_limit: int,
                         boolean_complexity_limit: int,
                         count_numerical_complexity_limit: int,
                         distance_numerical_complexity_limit: int,
                         feature_limit: int,
                         additional_booleans: List[str],
                         additional_numericals: List[str]):
    # Get concrete dlplan states of global states
    dlplan_ss_states = set()
    for instance_data in iteration_data.instance_datas:
        dlplan_ss_states.update(set(instance_data.dlplan_ss.get_states().values()))
    dlplan_ss_states = list(dlplan_ss_states)

    syntactic_element_factory = preprocessing_data.domain_data.syntactic_element_factory
    feature_generator = dlplan_generator.FeatureGenerator()
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
    if not disable_feature_generation:
        [generated_booleans, generated_numericals, _, _] = feature_generator.generate(
            syntactic_element_factory, list(dlplan_ss_states),
            concept_complexity_limit,
            role_complexity_limit,
            boolean_complexity_limit,
            count_numerical_complexity_limit,
            distance_numerical_complexity_limit,
            2147483647,  # max time limit,
            feature_limit)
        for numerical in generated_numericals:
            features.append(Feature(numerical, numerical.compute_complexity() + 1))
        for boolean in generated_booleans:
            features.append(Feature(boolean, boolean.compute_complexity() + 1 + 1))
    for numerical in additional_numericals:
        numerical = syntactic_element_factory.parse_numerical(numerical)
        features.append(Feature(numerical, numerical.compute_complexity() + 1))
    for boolean in additional_booleans:
        boolean = syntactic_element_factory.parse_boolean(boolean)
        features.append(Feature(boolean, boolean.compute_complexity() + 1 + 1))
    print("Features generated:", len(features))

    # Prune features that never reach 0/False
    selected_features = []
    for feature in features:
        always_nnz = True
        for instance_data in iteration_data.instance_datas:
            for dlplan_state in instance_data.dlplan_ss.get_states().values():
                val = int(feature.dlplan_feature.evaluate(dlplan_state, instance_data.denotations_caches))
                if val == 0:
                    always_nnz = False
                    break
        if not always_nnz:
            selected_features.append(feature)
    features = selected_features
    print("Features after 0/1 pruning (incomplete):", len(selected_features))

    # Prune features that decrease by more than 1 on a state transition
    soft_changing_features = set()
    for feature in features:
        is_soft_changing = True
        for instance_data in iteration_data.instance_datas:
            for s_idx in range(instance_data.mimir_ss.get_num_states()):
                dlplan_source = instance_data.dlplan_ss.get_states()[s_idx]
                source_val = int(feature.dlplan_feature.evaluate(dlplan_source, instance_data.denotations_caches))
                for s_prime_idx in instance_data.mimir_ss.get_forward_adjacent_state_indices(s_idx):
                    dlplan_target = instance_data.dlplan_ss.get_states()[s_prime_idx]
                    target_val = int(feature.dlplan_feature.evaluate(dlplan_target, instance_data.denotations_caches))
                    if source_val in {0, 2147483647} or target_val in {0, 2147483647}:
                        # Allow arbitrary changes on border values
                        continue
                    if source_val > target_val and (source_val > target_val + 1):
                        is_soft_changing = False
                        break
                    if target_val > source_val and (target_val > source_val + 1):
                        is_soft_changing = False
                        break
                if not is_soft_changing:
                        break
            if not is_soft_changing:
                break
        if is_soft_changing:
            soft_changing_features.add(feature)
    features = list(soft_changing_features)
    print("Features after soft changes pruning (incomplete):", len(features))

    # Prune features that do have same feature change a long all state pairs.
    feature_changes = dict()
    num_pruned = 0
    for feature in features:
        changes = []
        for instance_data in iteration_data.instance_datas:
            for s_idx, tuple_graph in preprocessing_data.ss_state_idx_to_tuple_graph[instance_data.idx].items():
                if instance_data.mimir_ss.is_deadend_state(s_idx):
                    continue

                dlplan_source = instance_data.dlplan_ss.get_states()[s_idx]
                source_val = int(feature.dlplan_feature.evaluate(dlplan_source, instance_data.denotations_caches))
                for s_primes in tuple_graph.get_states_grouped_by_distance():
                    for s_prime in s_primes:
                        s_prime_idx = instance_data.mimir_ss.get_state_index(s_prime)
                        dlplan_target = instance_data.dlplan_ss.get_states()[s_prime_idx]
                        target_val = int(feature.dlplan_feature.evaluate(dlplan_target, instance_data.denotations_caches))
                        if source_val < target_val:
                            changes.append(FeatureChange.UP)
                        elif source_val > target_val:
                            changes.append(FeatureChange.DOWN)
                        else:
                            changes.append(FeatureChange.BOT)
        existing_feature = feature_changes.get(tuple(changes), None)
        if existing_feature is None:
            feature_changes[tuple(changes)] = feature
        else:
            if existing_feature.complexity > feature.complexity:
                feature_changes[tuple(changes)] = feature
            num_pruned += 1
    features = list(feature_changes.values())
    print("Features after relevant changes pruning (complete):", len(features))

    return features
