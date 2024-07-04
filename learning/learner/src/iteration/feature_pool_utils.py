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
                         gfa_state_id_to_tuple_graph: Dict[int, mm.TupleGraph],
                         state_finder: StateFinder,
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
    for gfa_state in iteration_data.gfa_states:
        dlplan_ss_states.add(state_finder.get_dlplan_ss_state(gfa_state))
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
            syntactic_element_factory, dlplan_ss_states,
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
        for gfa_state in iteration_data.gfa_states:
            dlplan_source_ss_state = state_finder.get_dlplan_ss_state(gfa_state)
            instance_idx = gfa_state.get_abstraction_index()
            instance_data = preprocessing_data.instance_datas[instance_idx]
            source_val = int(feature.dlplan_feature.evaluate(dlplan_source_ss_state, instance_data.denotations_caches))

            gfa = instance_data.gfa
            gfa_state_idx = gfa.get_state_index(gfa_state)
            gfa_states = gfa.get_states()
            for gfa_state_prime_idx in gfa.get_target_states(gfa_state_idx):
                gfa_state_prime = gfa_states[gfa_state_prime_idx]
                dlplan_target_ss_state = state_finder.get_dlplan_ss_state(gfa_state_prime)
                target_val = int(feature.dlplan_feature.evaluate(dlplan_target_ss_state, instance_data.denotations_caches))
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
        if is_soft_changing:
            soft_changing_features.add(feature)
    features = list(soft_changing_features)
    print("Features after soft changes pruning (incomplete):", len(features))

    # Prune features that do have same feature change a long all state pairs.
    feature_changes = dict()
    num_pruned = 0
    for feature in features:
        changes = []
        for gfa_state in iteration_data.gfa_states:
            instance_idx = gfa_state.get_abstraction_index()
            instance_data = preprocessing_data.instance_datas[instance_idx]

            gfa_state_id = gfa_state.get_id()
            gfa_state_idx = state_finder.get_gfa_state_idx_from_gfa_state(gfa_state.get_abstraction_index(), gfa_state)
            if instance_data.gfa.is_deadend_state(gfa_state_idx):
                continue

            tuple_graph = gfa_state_id_to_tuple_graph[gfa_state_id]
            tuple_graph_vertices = tuple_graph.get_vertices()
            tuple_graph_vertices_by_distance = tuple_graph.get_vertex_indices_by_distances()

            dlplan_source_ss_state = state_finder.get_dlplan_ss_state(gfa_state)
            source_val = int(feature.dlplan_feature.evaluate(dlplan_source_ss_state, instance_data.denotations_caches))

            for tuple_vertex_idxs in tuple_graph_vertices_by_distance:
                for tuple_vertex_idx in tuple_vertex_idxs:
                    tuple_vertex = tuple_graph_vertices[tuple_vertex_idx]
                    for mimir_ss_state_prime in tuple_vertex.get_states():
                        gfa_state_prime = state_finder.get_gfa_state_from_ss_state_idx(instance_idx, instance_data.mimir_ss.get_state_index(mimir_ss_state_prime))
                        dlplan_target_ss_state = state_finder.get_dlplan_ss_state(gfa_state_prime)
                        instance_prime_idx = gfa_state_prime.get_abstraction_index()
                        instance_data_prime = preprocessing_data.instance_datas[instance_prime_idx]
                        target_val = int(feature.dlplan_feature.evaluate(dlplan_target_ss_state, instance_data_prime.denotations_caches))
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
