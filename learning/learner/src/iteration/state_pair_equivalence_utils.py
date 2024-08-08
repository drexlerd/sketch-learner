import math

from collections import defaultdict
from typing import List, Dict

import dlplan.core as dlplan_core
import dlplan.policy as dlplan_policy

from .state_pair_equivalence import StatePairEquivalence
from .feature_pool import Feature
from .iteration_data import IterationData

from ..preprocessing import PreprocessingData


def make_conditions(policy_builder: dlplan_policy.PolicyFactory,
    feature_pool: List[Feature],
    feature_valuations):
    """ Create conditions over all features that are satisfied in source_idx """
    conditions = set()
    for f_idx, (feature, val) in enumerate(zip(feature_pool, feature_valuations)):
        if isinstance(feature.dlplan_feature, dlplan_core.Boolean):
            if val:
                conditions.add(policy_builder.make_pos_condition(policy_builder.make_boolean(f"f{f_idx}", feature.dlplan_feature)))
            else:
                conditions.add(policy_builder.make_neg_condition(policy_builder.make_boolean(f"f{f_idx}", feature.dlplan_feature)))
        elif isinstance(feature.dlplan_feature, dlplan_core.Numerical):
            if val > 0:
                conditions.add(policy_builder.make_gt_condition(policy_builder.make_numerical(f"f{f_idx}", feature.dlplan_feature)))
            else:
                conditions.add(policy_builder.make_eq_condition(policy_builder.make_numerical(f"f{f_idx}", feature.dlplan_feature)))
    return conditions

def make_effects(policy_builder: dlplan_policy.PolicyFactory,
    feature_pool: List[Feature],
    source_feature_valuations,
    target_feature_valuations):
    """ Create effects over all features that are satisfied in (source_idx,target_idx) """
    effects = set()
    for f_idx, (feature, source_val, target_val) in enumerate(zip(feature_pool, source_feature_valuations, target_feature_valuations)):
        if isinstance(feature.dlplan_feature, dlplan_core.Boolean):
            if source_val and not target_val:
                effects.add(policy_builder.make_neg_effect(policy_builder.make_boolean(f"f{f_idx}", feature.dlplan_feature)))
            elif not source_val and target_val:
                effects.add(policy_builder.make_pos_effect(policy_builder.make_boolean(f"f{f_idx}", feature.dlplan_feature)))
            else:
                effects.add(policy_builder.make_bot_effect(policy_builder.make_boolean(f"f{f_idx}", feature.dlplan_feature)))
        elif isinstance(feature.dlplan_feature, dlplan_core.Numerical):
            if source_val > target_val:
                effects.add(policy_builder.make_dec_effect(policy_builder.make_numerical(f"f{f_idx}", feature.dlplan_feature)))
            elif source_val < target_val:
                effects.add(policy_builder.make_inc_effect(policy_builder.make_numerical(f"f{f_idx}", feature.dlplan_feature)))
            else:
                effects.add(policy_builder.make_bot_effect(policy_builder.make_numerical(f"f{f_idx}", feature.dlplan_feature)))
    return effects


def compute_state_pair_equivalences(preprocessing_data: PreprocessingData,
                                    iteration_data: IterationData):
    policy_builder = preprocessing_data.domain_data.policy_builder

    instance_idx_to_ss_idx_to_state_pair_equivalences: Dict[int, Dict[int, StatePairEquivalence]] = dict()

    # We have to take a new policy_builder because our feature pool F uses indices 0,...,|F|
    rules = []
    rule_repr_to_idx = dict()
    for instance_data in iteration_data.instance_datas:
        s_idx_to_state_pair_equivalence = dict()
        for s_idx, tuple_graph in preprocessing_data.ss_state_idx_to_tuple_graph[instance_data.idx].items():
            if instance_data.mimir_ss.is_deadend_state(s_idx):
                continue
            r_idx_to_distance = dict()
            r_idx_to_subgoal_states = defaultdict(set)
            subgoal_states_to_r_idx = dict()
            # add conditions

            conditions = make_conditions(policy_builder, iteration_data.feature_pool, iteration_data.instance_idx_to_ss_idx_to_feature_valuations[instance_data.idx][s_idx])
            for s_distance, s_primes in enumerate(tuple_graph.get_states_grouped_by_distance()):
                for s_prime in s_primes:
                    s_prime_idx = instance_data.mimir_ss.get_state_index(s_prime)
                    # add effects
                    effects = make_effects(policy_builder, iteration_data.feature_pool, iteration_data.instance_idx_to_ss_idx_to_feature_valuations[instance_data.idx][s_idx], iteration_data.instance_idx_to_ss_idx_to_feature_valuations[instance_data.idx][s_prime_idx])
                    # add rule
                    rule = policy_builder.make_rule(conditions, effects)
                    rule_repr = repr(rule)
                    if rule_repr in rule_repr_to_idx:
                        r_idx = rule_repr_to_idx[rule_repr]
                    else:
                        r_idx = len(rules)
                        rule_repr_to_idx[rule_repr] = r_idx
                        rules.append(rule)
                    r_idx_to_distance[r_idx] = min(r_idx_to_distance.get(r_idx, math.inf), s_distance)
                    r_idx_to_subgoal_states[r_idx].add(s_prime_idx)
                    subgoal_states_to_r_idx[s_prime_idx] = r_idx
            s_idx_to_state_pair_equivalence[s_idx] = StatePairEquivalence(r_idx_to_subgoal_states, r_idx_to_distance, subgoal_states_to_r_idx)
        instance_idx_to_ss_idx_to_state_pair_equivalences[instance_data.idx] = s_idx_to_state_pair_equivalence

    return rules, instance_idx_to_ss_idx_to_state_pair_equivalences
