from dlplan.policy import PolicyFactory
from dlplan.core import Boolean, Numerical

import math

from collections import defaultdict
from typing import List

from .state_pair_equivalence import StatePairEquivalenceClasses, StatePairEquivalence, PerStateStatePairEquivalences
from .feature_pool import FeaturePool
from .feature_valuations import FeatureValuations

from ..domain_data.domain_data import DomainData
from ..instance_data.instance_data import InstanceData




def make_conditions(policy_builder: PolicyFactory,
    feature_pool: FeaturePool,
    feature_valuations: FeatureValuations):
    """ Create conditions over all features that are satisfied in source_idx """
    conditions = set()
    for f_idx, (feature, val) in enumerate(zip(feature_pool.features, feature_valuations.feature_valuations)):
        if isinstance(feature.dlplan_feature, Boolean):
            if val:
                conditions.add(policy_builder.make_pos_condition(policy_builder.make_boolean(f"f{f_idx}", feature.dlplan_feature)))
            else:
                conditions.add(policy_builder.make_neg_condition(policy_builder.make_boolean(f"f{f_idx}", feature.dlplan_feature)))
        elif isinstance(feature.dlplan_feature, Numerical):
            if val > 0:
                conditions.add(policy_builder.make_gt_condition(policy_builder.make_numerical(f"f{f_idx}", feature.dlplan_feature)))
            else:
                conditions.add(policy_builder.make_eq_condition(policy_builder.make_numerical(f"f{f_idx}", feature.dlplan_feature)))
    return conditions

def make_effects(policy_builder: PolicyFactory,
    feature_pool: FeaturePool,
    source_feature_valuations: FeatureValuations,
    target_feature_valuations: FeatureValuations):
    """ Create effects over all features that are satisfied in (source_idx,target_idx) """
    effects = set()
    for f_idx, (feature, source_val, target_val) in enumerate(zip(feature_pool.features, source_feature_valuations.feature_valuations, target_feature_valuations.feature_valuations)):
        if isinstance(feature.dlplan_feature, Boolean):
            if source_val and not target_val:
                effects.add(policy_builder.make_neg_effect(policy_builder.make_boolean(f"f{f_idx}", feature.dlplan_feature)))
            elif not source_val and target_val:
                effects.add(policy_builder.make_pos_effect(policy_builder.make_boolean(f"f{f_idx}", feature.dlplan_feature)))
            else:
                effects.add(policy_builder.make_bot_effect(policy_builder.make_boolean(f"f{f_idx}", feature.dlplan_feature)))
        elif isinstance(feature.dlplan_feature, Numerical):
            if source_val > target_val:
                effects.add(policy_builder.make_dec_effect(policy_builder.make_numerical(f"f{f_idx}", feature.dlplan_feature)))
            elif source_val < target_val:
                effects.add(policy_builder.make_inc_effect(policy_builder.make_numerical(f"f{f_idx}", feature.dlplan_feature)))
            else:
                effects.add(policy_builder.make_bot_effect(policy_builder.make_numerical(f"f{f_idx}", feature.dlplan_feature)))
    return effects


def compute_state_pair_equivalences(domain_data: DomainData,
    instance_datas: List[InstanceData]):
    # We have to take a new policy_builder because our feature pool F uses indices 0,...,|F|
    policy_builder = domain_data.policy_builder
    rules = []
    rule_repr_to_idx = dict()
    for instance_data in instance_datas:
        s_idx_to_state_pair_equivalence = dict()
        for s_idx, tuple_graph in instance_data.per_state_tuple_graphs.s_idx_to_tuple_graph.items():
            if instance_data.is_deadend(s_idx):
                continue
            r_idx_to_distance = dict()
            r_idx_to_subgoal_states = defaultdict(set)
            subgoal_states_to_r_idx = dict()
            # add conditions
            conditions = make_conditions(policy_builder, domain_data.feature_pool, instance_data.per_state_feature_valuations.s_idx_to_feature_valuations[s_idx])
            for s_distance, s_prime_idxs in enumerate(tuple_graph.get_state_indices_by_distance()):
                for s_prime_idx in set(instance_data.state_index_to_representative_state_index[s] for s in s_prime_idxs):
                    # add effects
                    effects = make_effects(policy_builder, domain_data.feature_pool, instance_data.per_state_feature_valuations.s_idx_to_feature_valuations[s_idx], instance_data.per_state_feature_valuations.s_idx_to_feature_valuations[s_prime_idx])
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
        instance_data.per_state_state_pair_equivalences = PerStateStatePairEquivalences(s_idx_to_state_pair_equivalence)
    domain_data.domain_state_pair_equivalence = StatePairEquivalenceClasses(rules)
