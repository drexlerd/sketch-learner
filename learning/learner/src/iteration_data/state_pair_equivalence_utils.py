import math

from collections import defaultdict
from typing import List, Dict

import dlplan.core as dlplan_core
import dlplan.policy as dlplan_policy

from .state_pair_equivalence import StatePairEquivalence
from .feature_pool import Feature

from ..domain_data.domain_data import DomainData
from ..instance_data.instance_data import InstanceData, StateFinder


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


def compute_state_pair_equivalences(domain_data: DomainData,
    instance_datas: List[InstanceData],
    selected_instance_datas: List[InstanceData],
    state_finder: StateFinder):
    # We have to take a new policy_builder because our feature pool F uses indices 0,...,|F|
    policy_builder = domain_data.policy_builder
    rules = []
    rule_repr_to_idx = dict()

    gfa_state_id_to_state_pair_equivalence: Dict[int, StatePairEquivalence] = dict()

    for gfa_state in domain_data.gfa_states:
        instance_idx = gfa_state.get_abstraction_index()
        instance_data = instance_datas[instance_idx]
        gfa_state_id = gfa_state.get_id()
        gfa_state_idx = instance_data.gfa.get_state_index(gfa_state)
        if instance_data.gfa.is_deadend_state(gfa_state_idx):
            continue

        tuple_graph = domain_data.gfa_state_id_to_tuple_graph[gfa_state_id]

        r_idx_to_distance = dict()
        r_idx_to_subgoal_gfa_state_ids = defaultdict(set)
        subgoal_gfa_state_id_to_r_idx = dict()

        # add conditions
        conditions = make_conditions(policy_builder,
                                     domain_data.feature_pool,
                                     domain_data.gfa_state_id_to_feature_evaluations[gfa_state_id])

        for s_distance, mimir_ss_states_prime in enumerate(tuple_graph.get_states_by_distance()):
            for mimir_ss_state_prime in mimir_ss_states_prime:
                gfa_state_prime = state_finder.get_gfa_state_from_ss_state_idx(instance_idx, instance_data.mimir_ss.get_state_index(mimir_ss_state_prime))
                gfa_state_prime_id = gfa_state_prime.get_id()

                # add effects
                effects = make_effects(policy_builder,
                                        domain_data.feature_pool,
                                        domain_data.gfa_state_id_to_feature_evaluations[gfa_state_id],
                                        domain_data.gfa_state_id_to_feature_evaluations[gfa_state_prime_id])

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
                r_idx_to_subgoal_gfa_state_ids[r_idx].add(gfa_state_prime_id)
                subgoal_gfa_state_id_to_r_idx[gfa_state_prime_id] = r_idx

        gfa_state_id_to_state_pair_equivalence[gfa_state_id] = StatePairEquivalence(r_idx_to_subgoal_gfa_state_ids, r_idx_to_distance, subgoal_gfa_state_id_to_r_idx)

    domain_data.state_pair_equivalences = rules
    domain_data.gfa_state_id_to_state_pair_equivalence = gfa_state_id_to_state_pair_equivalence
