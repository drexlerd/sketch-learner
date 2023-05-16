import dlplan
import math

from collections import defaultdict
from dataclasses import dataclass
from typing import List

from learner.src.domain_data.domain_data import DomainData
from learner.src.instance_data.instance_data import InstanceData
from learner.src.iteration_data.state_pair_equivalence import DomainStatePairEquivalence, StatePairEquivalence
from learner.src.iteration_data.domain_feature_data import DomainFeatureData
from learner.src.iteration_data.feature_valuations import StateFeatureValuation


@dataclass
class StatePairEquivalenceStatistics:
    num_subgoal_states: int = 0
    num_equivalences: int = 0

    def increment_num_subgoal_states(self):
        self.num_subgoal_states += 1

    def increment_num_equivalences(self):
        self.num_equivalences += 1

    def print(self):
        print("StatePairEquivalenceStatistics:")
        print("    num_subgoal_states:", self.num_subgoal_states)
        print("    num_equivalences:", self.num_equivalences)


class StatePairEquivalenceFactory:
    def __init__(self):
        self.statistics = StatePairEquivalenceStatistics()

    def make_state_pair_equivalences(self,
        domain_data: DomainData,
        instance_datas: List[InstanceData]):
        # We have to take a new policy_builder because our feature pool F uses indices 0,...,|F|
        policy_builder = domain_data.policy_builder
        rules = []
        rule_repr_to_idx = dict()
        for instance_data in instance_datas:
            state_pair_equivalences = dict()
            for s_idx, tuple_graph in instance_data.tuple_graphs.items():
                if instance_data.is_deadend(s_idx):
                    continue
                r_idx_to_distance = dict()
                r_idx_to_subgoal_states = defaultdict(set)
                subgoal_states_to_r_idx = dict()
                # add conditions
                conditions = self._make_conditions(policy_builder, domain_data.domain_feature_data, instance_data.feature_valuations[s_idx])
                for d, s_prime_idxs in enumerate(tuple_graph.get_state_indices_by_distance()):
                    for s_prime_idx in s_prime_idxs:
                        self.statistics.increment_num_subgoal_states()
                        # add effects
                        effects = self._make_effects(policy_builder, domain_data.domain_feature_data, instance_data.feature_valuations[s_idx], instance_data.feature_valuations[s_prime_idx])
                        # add rule
                        rule = policy_builder.add_rule(conditions, effects)
                        rule_repr = rule.compute_repr()
                        if rule_repr in rule_repr_to_idx:
                            r_idx = rule_repr_to_idx[rule_repr]
                        else:
                            self.statistics.increment_num_equivalences()
                            r_idx = len(rules)
                            rule_repr_to_idx[rule_repr] = r_idx
                            rules.append(rule)
                        r_idx_to_distance[r_idx] = min(r_idx_to_distance.get(r_idx, math.inf), d)
                        r_idx_to_subgoal_states[r_idx].add(s_prime_idx)
                        subgoal_states_to_r_idx[s_prime_idx] = r_idx
                state_pair_equivalences[s_idx] = StatePairEquivalence(r_idx_to_subgoal_states, r_idx_to_distance, subgoal_states_to_r_idx)
                # state_pair_equivalences[s_idx].print()
            instance_data.set_state_pair_equivalences(state_pair_equivalences)
        domain_data.domain_state_pair_equivalence = DomainStatePairEquivalence(rules)

    def _make_conditions(self,
        policy_builder: dlplan.PolicyBuilder,
        domain_feature_data: DomainFeatureData,
        feature_valuations: StateFeatureValuation):
        """ Create conditions over all features that are satisfied in source_idx """
        conditions = set()
        for b_idx, boolean in domain_feature_data.boolean_features.f_idx_to_feature.items():
            val = feature_valuations.b_idx_to_val[b_idx]
            if val:
                conditions.add(policy_builder.add_pos_condition(boolean.dlplan_feature))
            else:
                conditions.add(policy_builder.add_neg_condition(boolean.dlplan_feature))
        for n_idx, numerical in domain_feature_data.numerical_features.f_idx_to_feature.items():
            val = feature_valuations.n_idx_to_val[n_idx]
            if val > 0:
                conditions.add(policy_builder.add_gt_condition(numerical.dlplan_feature))
            else:
                conditions.add(policy_builder.add_eq_condition(numerical.dlplan_feature))
        return conditions

    def _make_effects(self,
        policy_builder: dlplan.PolicyBuilder,
        domain_feature_data: DomainFeatureData,
        source_feature_valuations: StateFeatureValuation,
        target_feature_valuations: StateFeatureValuation):
        """ Create effects over all features that are satisfied in (source_idx,target_idx) """
        effects = set()
        for b_idx, boolean in domain_feature_data.boolean_features.f_idx_to_feature.items():
            source_val = source_feature_valuations.b_idx_to_val[b_idx]
            target_val = target_feature_valuations.b_idx_to_val[b_idx]
            if source_val and not target_val:
                effects.add(policy_builder.add_neg_effect(boolean.dlplan_feature))
            elif not source_val and target_val:
                effects.add(policy_builder.add_pos_effect(boolean.dlplan_feature))
            else:
                effects.add(policy_builder.add_bot_effect(boolean.dlplan_feature))
        for n_idx, numerical in domain_feature_data.numerical_features.f_idx_to_feature.items():
            source_val = source_feature_valuations.n_idx_to_val[n_idx]
            target_val = target_feature_valuations.n_idx_to_val[n_idx]
            if source_val > target_val:
                effects.add(policy_builder.add_dec_effect(numerical.dlplan_feature))
            elif source_val < target_val:
                effects.add(policy_builder.add_inc_effect(numerical.dlplan_feature))
            else:
                effects.add(policy_builder.add_bot_effect(numerical.dlplan_feature))
        return effects
