import dlplan

from collections import defaultdict
from dataclasses import dataclass
from typing import List

from .state_pair_equivalence import DomainStatePairEquivalence, InstanceStatePairEquivalence
from .domain_feature_data import DomainFeatureData

from ..instance_data.state_pair import StatePair
from ..instance_data.instance_data import InstanceData


@dataclass
class StatePairEquivalenceStatistics:
    num_state_pairs: int = 0
    num_equivalences: int = 0

    def increment_num_state_pairs(self):
        self.num_state_pairs += 1

    def increment_num_equivalences(self):
        self.num_equivalences += 1

    def print(self):
        print("StatePairEquivalenceStatistics:")
        print("    num_state_pairs:", self.num_state_pairs)
        print("    num_equivalences:", self.num_equivalences)


class StatePairEquivalenceFactory:
    def __init__(self):
        self.statistics = StatePairEquivalenceStatistics()

    def make_state_pair_equivalences(self, domain_feature_data: DomainFeatureData, instance_datas: List[InstanceData]):
        policy_builder = dlplan.PolicyBuilder()
        policy_boolean_features = [policy_builder.add_boolean_feature(b) for b in domain_feature_data.boolean_features]
        policy_numerical_features = [policy_builder.add_numerical_feature(n) for n in domain_feature_data.numerical_features]
        rules = []
        rule_repr_to_idx = dict()
        for instance_data in instance_datas:
            r_idx_to_state_pairs = defaultdict(set)
            state_pair_to_r_idx = dict()
            r_idx_to_state_class_pairs = defaultdict(set)
            state_class_pair_to_r_idx = dict()
            for s_idx, tuple_graph in instance_data.tuple_graphs.items():
                # add conditions
                conditions = self._make_conditions(policy_builder, policy_boolean_features, policy_numerical_features, instance_data.feature_valuations[s_idx])
                for s_prime_idxs in tuple_graph.get_state_indices_by_distance():
                    for s_prime_idx in s_prime_idxs:
                        state_pair = StatePair(s_idx, s_prime_idx)
                        self.statistics.increment_num_state_pairs()
                        # add effects
                        effects = self._make_effects(policy_builder, policy_boolean_features, policy_numerical_features, instance_data.feature_valuations[s_idx], instance_data.feature_valuations[s_prime_idx])
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
                        r_idx_to_state_pairs[r_idx].add(state_pair)
                        state_pair_to_r_idx[state_pair] = r_idx
                        state_class_pair = (instance_data.state_equivalence.s_idx_to_state_class_idx[s_idx],
                            instance_data.state_equivalence.s_idx_to_state_class_idx[s_prime_idx])
                        r_idx_to_state_class_pairs[r_idx].add(state_class_pair)
                        state_class_pair_to_r_idx[state_class_pair] = r_idx
            instance_data.set_state_pair_equivalence(InstanceStatePairEquivalence(r_idx_to_state_pairs, state_pair_to_r_idx, r_idx_to_state_class_pairs, state_class_pair_to_r_idx))
        return DomainStatePairEquivalence(rules)

    def _make_conditions(self, policy_builder: dlplan.PolicyBuilder, policy_boolean_features, policy_numerical_features, feature_valuations):
        """ Create conditions over all features that are satisfied in source_idx """
        conditions = []
        boolean_feature_valuations = feature_valuations.boolean_feature_valuations
        numerical_feature_valuations = feature_valuations.numerical_feature_valuations
        for n_idx in range(len(policy_numerical_features)):
            if numerical_feature_valuations[n_idx] > 0:
                conditions.append(policy_builder.add_gt_condition(policy_numerical_features[n_idx]))
            else:
                conditions.append(policy_builder.add_eq_condition(policy_numerical_features[n_idx]))
        for b_idx in range(len(policy_boolean_features)):
            if boolean_feature_valuations[b_idx]:
                conditions.append(policy_builder.add_pos_condition(policy_boolean_features[b_idx]))
            else:
                conditions.append(policy_builder.add_neg_condition(policy_boolean_features[b_idx]))
        return conditions

    def _make_effects(self, policy_builder: dlplan.PolicyBuilder, policy_boolean_features, policy_numerical_features, source_feature_valuations, target_feature_valuations):
        """ Create effects over all features that are satisfied in (source_idx,target_idx) """
        effects = []
        for n_idx in range(len(policy_numerical_features)):
            if source_feature_valuations.numerical_feature_valuations[n_idx] > target_feature_valuations.numerical_feature_valuations[n_idx]:
                effects.append(policy_builder.add_dec_effect(policy_numerical_features[n_idx]))
            elif source_feature_valuations.numerical_feature_valuations[n_idx] < target_feature_valuations.numerical_feature_valuations[n_idx]:
                effects.append(policy_builder.add_inc_effect(policy_numerical_features[n_idx]))
            else:
                effects.append(policy_builder.add_bot_effect(policy_numerical_features[n_idx]))
        for b_idx in range(len(policy_boolean_features)):
            if source_feature_valuations.boolean_feature_valuations[b_idx] and not target_feature_valuations.boolean_feature_valuations[b_idx]:
                effects.append(policy_builder.add_neg_effect(policy_boolean_features[b_idx]))
            elif not source_feature_valuations.boolean_feature_valuations[b_idx] and target_feature_valuations.boolean_feature_valuations[b_idx]:
                effects.append(policy_builder.add_pos_effect(policy_boolean_features[b_idx]))
            else:
                effects.append(policy_builder.add_bot_effect(policy_boolean_features[b_idx]))
        return effects
