import dlplan
from clingo import Symbol
from typing import  List

from sketch_learning.iteration_data.state_pair_equivalence import DomainStatePairEquivalence

from .domain_feature_data import DomainFeatureData


class DlplanPolicyFactory:
    def make_dlplan_policy_from_answer_set(self, symbols: List[Symbol], domain_feature_data: DomainFeatureData):
        """ Parses set of facts from ASP that contains rules into dlplan.Policy """
        policy_builder = dlplan.PolicyBuilder()
        f_idx_to_policy_feature = self._add_features(policy_builder, symbols, domain_feature_data)
        self._add_rules(policy_builder, symbols, f_idx_to_policy_feature)
        return policy_builder.get_result()

    def make_dlplan_policy_from_answer_set_d2(self, symbols: List[Symbol], domain_feature_data: DomainFeatureData, rule_equivalences: DomainStatePairEquivalence):
        """ Parses set of facts from ASP that contains D2 constraints into dlplan.Policy """
        policy_builder = dlplan.PolicyBuilder()
        f_idx_to_policy_feature = self._add_features(policy_builder, symbols, domain_feature_data)
        self._add_rules_d2(policy_builder, symbols, f_idx_to_policy_feature, rule_equivalences)
        return policy_builder.get_result()

    def _add_features(self, policy_builder: dlplan.PolicyBuilder, symbols: List[Symbol], domain_feature_data: DomainFeatureData):
        f_idx_to_policy_feature = dict()
        for symbol in symbols:
            if symbol.name == "select":
                f_idx = symbol.arguments[0].number
                if f_idx < len(domain_feature_data.boolean_features):
                    f_idx_to_policy_feature[f_idx] = policy_builder.add_boolean_feature(domain_feature_data.boolean_features[f_idx])
                else:
                    f_idx_to_policy_feature[f_idx] = policy_builder.add_numerical_feature(domain_feature_data.numerical_features[f_idx - len(domain_feature_data.boolean_features)])
        return f_idx_to_policy_feature


    def _add_rules_d2(self, policy_builder: dlplan.PolicyBuilder, symbols: List[Symbol], f_idx_to_policy_feature, rule_equivalence_data: DomainStatePairEquivalence):
        rules = dict()
        for symbol in symbols:
            if symbol.name == "good":
                r_idx = symbol.arguments[0].number
                rules[r_idx] = [[], []]  # conditions and effects
        for symbol in symbols:
            if symbol.name == "feature_condition":
                f_idx = symbol.arguments[0].number
                r_idx = symbol.arguments[1].number
                condition = symbol.arguments[2].number
                if f_idx not in f_idx_to_policy_feature: continue
                if r_idx not in rules: continue
                if condition == 0:
                    rules[r_idx][0].append(policy_builder.add_pos_condition(f_idx_to_policy_feature[f_idx]))
                elif condition == 1:
                    rules[r_idx][0].append(policy_builder.add_neg_condition(f_idx_to_policy_feature[f_idx]))
                elif condition == 2:
                    rules[r_idx][0].append(policy_builder.add_gt_condition(f_idx_to_policy_feature[f_idx]))
                elif condition == 3:
                    rules[r_idx][0].append(policy_builder.add_eq_condition(f_idx_to_policy_feature[f_idx]))
                else:
                    pass
            elif symbol.name == "feature_effect":
                f_idx = symbol.arguments[0].number
                r_idx = symbol.arguments[1].number
                effect = symbol.arguments[2].number
                if f_idx not in f_idx_to_policy_feature: continue
                if r_idx not in rules: continue
                if effect == 0:
                    rules[r_idx][1].append(policy_builder.add_pos_effect(f_idx_to_policy_feature[f_idx]))
                elif effect == 1:
                    rules[r_idx][1].append(policy_builder.add_neg_effect(f_idx_to_policy_feature[f_idx]))
                elif effect == 2:
                    rules[r_idx][1].append(policy_builder.add_bot_effect(f_idx_to_policy_feature[f_idx]))
                elif effect == 3:
                    rules[r_idx][1].append(policy_builder.add_inc_effect(f_idx_to_policy_feature[f_idx]))
                elif effect == 4:
                    rules[r_idx][1].append(policy_builder.add_dec_effect(f_idx_to_policy_feature[f_idx]))
                elif effect == 5:
                    rules[r_idx][1].append(policy_builder.add_bot_effect(f_idx_to_policy_feature[f_idx]))
                else:
                    pass
        for _, (conditions, effects) in rules.items():
            policy_builder.add_rule(conditions, effects)
