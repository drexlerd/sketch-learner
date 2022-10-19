import dlplan
from clingo import Symbol
from typing import  List

from sketch_learning.iteration_data.state_pair_equivalence import DomainStatePairEquivalence

from .domain_feature_data import DomainFeatureData


class DlplanPolicyFactory:
    def make_dlplan_policy_from_answer_set(self, symbols: List[Symbol], domain_feature_data: DomainFeatureData, rule_equivalence: DomainStatePairEquivalence):
        """ Parses set of facts from ASP that contains rules into dlplan.Policy """
        policy_builder = dlplan.PolicyBuilder()
        selected_feature_reprs = set()
        for symbol in symbols:
            if symbol.name == "select":
                f_idx = symbol.arguments[0].number
                if f_idx < len(domain_feature_data.boolean_features):
                    selected_feature_reprs.add(domain_feature_data.boolean_features[f_idx].compute_repr())
                else:
                    selected_feature_reprs.add(domain_feature_data.numerical_features[f_idx - len(domain_feature_data.boolean_features)].compute_repr())
        for symbol in symbols:
            if symbol.name == "good":
                r_idx = symbol.arguments[0].number
                rule = rule_equivalence.rules[r_idx]
                conditions = []
                for condition in rule.get_conditions():
                    if condition.get_base_feature().compute_repr() in selected_feature_reprs:
                        new_condition = condition.copy_to_builder(policy_builder)
                        conditions.append(new_condition)
                effects = []
                for effect in rule.get_effects():
                    if effect.get_base_feature().compute_repr() in selected_feature_reprs:
                        new_effect = effect.copy_to_builder(policy_builder)
                        effects.append(new_effect)
                policy_builder.add_rule(conditions, effects)
        return policy_builder.get_result()
