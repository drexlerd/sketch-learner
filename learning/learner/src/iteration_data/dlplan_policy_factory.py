import re

from abc import ABC, abstractmethod

from dlplan.policy import PolicyFactory
from clingo import Symbol
from typing import List

from learner.src.domain_data.domain_data import DomainData


class DlplanPolicyFactory(ABC):
    """ """
    @abstractmethod
    def make_dlplan_policy_from_answer_set(self, symbols: List[Symbol], domain_data: DomainData):
        """
        Parses the facts of an answer set into a dlplan policy.
        """


def extract_f_idx_from_argument(string: str):
    """
    Input examples: n1231 for numerical or b123 for boolean
    with respective outputs 1231 and 123.
    """
    return int(re.findall(r"[bn](.+)", string)[0])


class ExplicitDlplanPolicyFactory(DlplanPolicyFactory):
    """
    Encoding where rules are explicit in the ASP encoding (ICAPS2022)
    """
    def make_dlplan_policy_from_answer_set(self, symbols: List[Symbol], domain_data: DomainData):
        """ """
        policy_builder = domain_data.policy_builder
        f_idx_to_dlplan_boolean, f_idx_to_dlplan_numerical = self._add_features(symbols, domain_data)
        rules = self._add_rules(policy_builder, symbols, f_idx_to_dlplan_boolean, f_idx_to_dlplan_numerical)
        policy = policy_builder.add_policy(rules)
        return policy

    def _add_features(self, symbols: List[Symbol], domain_data: DomainData):
        """ """
        f_idx_to_dlplan_boolean = dict()
        f_idx_to_dlplan_numerical = dict()
        for symbol in symbols:
            if symbol.name == "select":
                if symbol.arguments[0].string[0] == "b":
                    f_idx = extract_f_idx_from_argument(symbol.arguments[0].string)
                    f_idx_to_dlplan_boolean[f_idx] = domain_data.feature_pool.boolean_features.f_idx_to_feature[f_idx].dlplan_feature
                elif symbol.arguments[0].string[0] == "n":
                    f_idx = extract_f_idx_from_argument(symbol.arguments[0].string)
                    f_idx_to_dlplan_numerical[f_idx] = domain_data.feature_pool.numerical_features.f_idx_to_feature[f_idx].dlplan_feature
        return f_idx_to_dlplan_boolean, f_idx_to_dlplan_numerical

    def _add_rules(self, policy_builder: PolicyFactory, symbols: List[Symbol], f_idx_to_dlplan_boolean, f_idx_to_dlplan_numerical):
        """ """
        rules_dict = dict()
        for symbol in symbols:
            if symbol.name == "rule":
                r_idx = symbol.arguments[0].number
                rules_dict[r_idx] = [set(), set()]  # conditions and effects
        for symbol in symbols:
            if symbol.name in {"c_eq", "c_gt", "c_pos", "c_neg", "e_inc", "e_dec", "e_pos", "e_neg", "e_bot"}:
                r_idx = symbol.arguments[0].number
                f_idx = extract_f_idx_from_argument(symbol.arguments[1].string)
                if symbol.arguments[1].string[0] == "b" and f_idx in f_idx_to_dlplan_boolean:
                    if symbol.name == "c_pos":
                        rules_dict[r_idx][0].add(policy_builder.add_pos_condition(f_idx_to_dlplan_boolean[f_idx]))
                    elif symbol.name == "c_neg":
                        rules_dict[r_idx][0].add(policy_builder.add_neg_condition(f_idx_to_dlplan_boolean[f_idx]))
                    elif symbol.name == "e_pos":
                        rules_dict[r_idx][1].add(policy_builder.add_pos_effect(f_idx_to_dlplan_boolean[f_idx]))
                    elif symbol.name == "e_neg":
                        rules_dict[r_idx][1].add(policy_builder.add_neg_effect(f_idx_to_dlplan_boolean[f_idx]))
                    elif symbol.name == "e_bot":
                        rules_dict[r_idx][1].add(policy_builder.add_bot_effect(f_idx_to_dlplan_boolean[f_idx]))
                if symbol.arguments[1].string[0] == "n" and f_idx in f_idx_to_dlplan_numerical:
                    if symbol.name == "c_eq":
                        rules_dict[r_idx][0].add(policy_builder.add_eq_condition(f_idx_to_dlplan_numerical[f_idx]))
                    elif symbol.name == "c_gt":
                        rules_dict[r_idx][0].add(policy_builder.add_gt_condition(f_idx_to_dlplan_numerical[f_idx]))
                    elif symbol.name == "e_inc":
                        rules_dict[r_idx][1].add(policy_builder.add_inc_effect(f_idx_to_dlplan_numerical[f_idx]))
                    elif symbol.name == "e_dec":
                        rules_dict[r_idx][1].add(policy_builder.add_dec_effect(f_idx_to_dlplan_numerical[f_idx]))
                    elif symbol.name == "e_bot":
                        rules_dict[r_idx][1].add(policy_builder.add_bot_effect(f_idx_to_dlplan_numerical[f_idx]))
        rules = set()
        for _, (conditions, effects) in rules_dict.items():
            rules.add(policy_builder.make_rule(conditions, effects))
        return rules


class D2sepDlplanPolicyFactory(DlplanPolicyFactory):
    """
    Encoding where rules are implicit in the D2-separation.
    """
    def make_dlplan_policy_from_answer_set(self, symbols: List[Symbol], domain_data: DomainData):
        policy_builder = domain_data.policy_builder
        dlplan_features = set()
        for symbol in symbols:
            if symbol.name == "select":
                if symbol.arguments[0].string[0] == "b":
                    f_idx = extract_f_idx_from_argument(symbol.arguments[0].string)
                    dlplan_features.add(domain_data.feature_pool.boolean_features.f_idx_to_feature[f_idx].dlplan_feature)
                elif symbol.arguments[0].string[0] == "n":
                    f_idx = extract_f_idx_from_argument(symbol.arguments[0].string)
                    dlplan_features.add(domain_data.feature_pool.numerical_features.f_idx_to_feature[f_idx].dlplan_feature)
        rules = set()
        for symbol in symbols:
            if symbol.name == "good":
                r_idx = symbol.arguments[0].number
                rule = domain_data.domain_state_pair_equivalence.rules[r_idx]
                conditions = set()
                for condition in rule.get_conditions():
                    result = re.findall(r"\(.* (\d+)\)", str(condition))
                    f_idx = int(result[0])
                    assert len(result) == 1
                    assert not (f_idx in domain_data.feature_pool.boolean_features.f_idx_to_feature and f_idx in domain_data.feature_pool.numerical_features.f_idx_to_feature)
                    if f_idx in domain_data.feature_pool.boolean_features.f_idx_to_feature:
                        feature = domain_data.feature_pool.boolean_features.f_idx_to_feature[f_idx].dlplan_feature
                    if f_idx in domain_data.feature_pool.numerical_features.f_idx_to_feature:
                        feature = domain_data.feature_pool.numerical_features.f_idx_to_feature[f_idx].dlplan_feature
                    if feature in dlplan_features:
                        conditions.add(condition)
                effects = set()
                for effect in rule.get_effects():
                    result = re.findall(r"\(.* (\d+)\)", str(effect))
                    f_idx = int(result[0])
                    assert len(result) == 1
                    if f_idx in domain_data.feature_pool.boolean_features.f_idx_to_feature:
                        feature = domain_data.feature_pool.boolean_features.f_idx_to_feature[f_idx].dlplan_feature
                    if f_idx in domain_data.feature_pool.numerical_features.f_idx_to_feature:
                        feature = domain_data.feature_pool.numerical_features.f_idx_to_feature[f_idx].dlplan_feature
                    if feature in dlplan_features:
                        effects.add(effect)
                rules.add(policy_builder.make_rule(conditions, effects))
        return policy_builder.make_policy(rules)
