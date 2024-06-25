import re

from abc import ABC, abstractmethod

import dlplan.core as dlplan_core

from clingo import Symbol
from typing import List, Union, MutableSet

from .iteration_data import IterationData

from ..preprocessing import PreprocessingData


class DlplanPolicyFactory(ABC):
    """ """
    @abstractmethod
    def make_dlplan_policy_from_answer_set(self, symbols: List[Symbol], preprocssing_data: PreprocessingData, iteration_data: IterationData):
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
    def make_dlplan_policy_from_answer_set(self, symbols: List[Symbol], preprocessing_data: PreprocessingData, iteration_data: IterationData):
        """ """
        policy_builder = preprocessing_data.domain_data.policy_builder
        selected_features = self._add_features(symbols, preprocessing_data, iteration_data)
        rules = self._add_rules(symbols, preprocessing_data, iteration_data, selected_features)
        return policy_builder.make_policy(rules)

    def _add_features(self, symbols: List[Symbol], preprocessing_data: PreprocessingData, iteration_data: IterationData):
        """ """
        selected_features = set()
        for symbol in symbols:
            if symbol.name == "select":
                f_idx = symbol.arguments[0].number
                selected_features.add(iteration_data.feature_pool[f_idx].dlplan_feature)
        return selected_features

    def _add_rules(self, symbols: List[Symbol], preprocessing_data: PreprocessingData, iteration_data: IterationData, selected_features: MutableSet[Union[dlplan_core.Boolean, dlplan_core.Numerical]]):
        """ """
        policy_builder = preprocessing_data.domain_data.policy_builder
        rules_dict = dict()
        for symbol in symbols:
            if symbol.name == "rule":
                r_idx = symbol.arguments[0].number
                rules_dict[r_idx] = [set(), set()]  # conditions and effects
        for symbol in symbols:
            if symbol.name in {"c_b_pos", "c_b_neg", "c_n_gt", "c_n_eq", "e_b_pos", "e_b_neg", "e_b_bot", "e_n_dec", "e_n_inc", "e_n_bot"}:
                r_idx = symbol.arguments[0].number
                f_idx = symbol.arguments[1].number
                feature = iteration_data.feature_pool[f_idx].dlplan_feature
                if feature not in selected_features:
                    continue
                if symbol.name == "c_b_pos":
                    rules_dict[r_idx][0].add(policy_builder.make_pos_condition(policy_builder.make_boolean(f"f{f_idx}", feature)))
                elif symbol.name == "c_b_neg":
                    rules_dict[r_idx][0].add(policy_builder.make_neg_condition(policy_builder.make_boolean(f"f{f_idx}", feature)))
                elif symbol.name == "c_n_gt":
                    rules_dict[r_idx][0].add(policy_builder.make_gt_condition(policy_builder.make_numerical(f"f{f_idx}", feature)))
                elif symbol.name == "c_n_eq":
                    rules_dict[r_idx][0].add(policy_builder.make_eq_condition(policy_builder.make_numerical(f"f{f_idx}", feature)))
                elif symbol.name == "e_b_pos":
                    rules_dict[r_idx][1].add(policy_builder.make_pos_effect(policy_builder.make_boolean(f"f{f_idx}", feature)))
                elif symbol.name == "e_b_neg":
                    rules_dict[r_idx][1].add(policy_builder.make_neg_effect(policy_builder.make_boolean(f"f{f_idx}", feature)))
                elif symbol.name == "e_b_bot":
                    rules_dict[r_idx][1].add(policy_builder.make_bot_effect(policy_builder.make_boolean(f"f{f_idx}", feature)))
                elif symbol.name == "e_n_dec":
                    rules_dict[r_idx][1].add(policy_builder.make_dec_effect(policy_builder.make_numerical(f"f{f_idx}", feature)))
                elif symbol.name == "e_n_inc":
                    rules_dict[r_idx][1].add(policy_builder.make_inc_effect(policy_builder.make_numerical(f"f{f_idx}", feature)))
                elif symbol.name == "e_n_bot":
                    rules_dict[r_idx][1].add(policy_builder.make_bot_effect(policy_builder.make_numerical(f"f{f_idx}", feature)))
        rules = set()
        for _, (conditions, effects) in rules_dict.items():
            rules.add(policy_builder.make_rule(conditions, effects))
        return rules


class D2sepDlplanPolicyFactory(DlplanPolicyFactory):
    """
    Encoding where rules are implicit in the D2-separation.
    """
    def make_dlplan_policy_from_answer_set(self, symbols: List[Symbol], preprocessing_data: PreprocessingData, iteration_data: IterationData):
        policy_builder = preprocessing_data.domain_data.policy_builder
        dlplan_features = set()
        for symbol in symbols:
            if symbol.name == "select":
                f_idx = symbol.arguments[0].number
                dlplan_features.add(iteration_data.feature_pool[f_idx].dlplan_feature)
        rules = set()
        for symbol in symbols:
            if symbol.name == "good":
                r_idx = symbol.arguments[0].number
                rule = iteration_data.state_pair_equivalences[r_idx]
                conditions = set()
                for condition in rule.get_conditions():
                    f_idx = int(condition.get_named_element().get_key()[1:])
                    dlplan_feature = iteration_data.feature_pool[f_idx].dlplan_feature
                    if dlplan_feature in dlplan_features:
                        conditions.add(condition)
                effects = set()
                for effect in rule.get_effects():
                    f_idx = int(effect.get_named_element().get_key()[1:])
                    dlplan_feature = iteration_data.feature_pool[f_idx].dlplan_feature
                    if dlplan_feature in dlplan_features:
                        effects.add(effect)
                rules.add(policy_builder.make_rule(conditions, effects))
        return policy_builder.make_policy(rules)
