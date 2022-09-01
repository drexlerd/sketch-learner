import re
from clingo import String, Number

from ....iteration_data.state_pair_equivalence import RuleEquivalences
from ....iteration_data.domain_feature_data import DomainFeatureData


class EquivalenceDataFactFactory():
    def make_facts(self, rule_equivalences: RuleEquivalences, domain_feature_data: DomainFeatureData):
        facts = []
        for r_idx, rule in enumerate(rule_equivalences.rules):
            facts.append(("equivalence", [Number(r_idx)]))
            for condition in rule.get_conditions():
                condition_str = condition.str()
                result = re.findall(r"\(.* (\d+)\)", condition_str)
                assert len(result) == 1
                f_idx = int(result[0])
                if condition_str.startswith("(:c_b_pos"):
                    facts.append(("feature_condition", [Number(f_idx), Number(r_idx), Number(0)]))
                elif condition_str.startswith("(:c_b_neg"):
                    facts.append(("feature_condition", [Number(f_idx), Number(r_idx), Number(1)]))
                elif condition_str.startswith("(:c_n_gt"):
                    facts.append(("feature_condition", [Number(f_idx + len(domain_feature_data.boolean_features)), Number(r_idx), Number(2)]))
                elif condition_str.startswith("(:c_n_eq"):
                    facts.append(("feature_condition", [Number(f_idx + len(domain_feature_data.boolean_features)), Number(r_idx), Number(3)]))
                else:
                    raise Exception(f"Cannot parse condition {condition_str}")
            for effect in rule.get_effects():
                effect_str = effect.str()
                result = re.findall(r"\(.* (\d+)\)", effect_str)
                assert len(result) == 1
                f_idx = int(result[0])
                if effect_str.startswith("(:e_b_pos"):
                    facts.append(("feature_effect", [Number(f_idx), Number(r_idx), Number(0)]))
                elif effect_str.startswith("(:e_b_neg"):
                    facts.append(("feature_effect", [Number(f_idx), Number(r_idx), Number(1)]))
                elif effect_str.startswith("(:e_b_bot"):
                    facts.append(("feature_effect", [Number(f_idx), Number(r_idx), Number(2)]))
                elif effect_str.startswith("(:e_n_inc"):
                    facts.append(("feature_effect", [Number(f_idx + len(domain_feature_data.boolean_features)), Number(r_idx), Number(3)]))
                elif effect_str.startswith("(:e_n_dec"):
                    facts.append(("feature_effect", [Number(f_idx + len(domain_feature_data.boolean_features)), Number(r_idx), Number(4)]))
                elif effect_str.startswith("(:e_n_bot"):
                    facts.append(("feature_effect", [Number(f_idx + len(domain_feature_data.boolean_features)), Number(r_idx), Number(5)]))
                else:
                    raise Exception(f"Cannot parse effect {effect_str}")
        return facts