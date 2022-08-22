import re
from clingo import String, Number

from ....iteration_data.state_pair_equivalence_data import RuleEquivalenceData
from ....iteration_data.domain_feature_data import DomainFeatureData


class EquivalenceDataFactFactory():
    def make_facts(self, rule_equivalence_data: RuleEquivalenceData, domain_feature_data: DomainFeatureData):
        facts = []
        for r_idx, rule in enumerate(rule_equivalence_data.rules):
            facts.append(("equivalence", [Number(r_idx)]))
            for condition in rule.get_conditions():
                condition_str = condition.str()
                result = re.findall(r"\(.* (\d+)\)", condition_str)
                assert len(result) == 1
                f_idx = int(result[0])
                if condition_str.startswith("(:c_b_pos"): facts.append(("c_pos_fixed", [Number(r_idx), Number(f_idx)]))
                elif condition_str.startswith("(:c_b_neg"): facts.append(("c_neg_fixed", [Number(r_idx), Number(f_idx)]))
                elif condition_str.startswith("(:c_n_gt"): facts.append(("c_gt_fixed", [Number(r_idx), Number(f_idx + len(domain_feature_data.boolean_features))]))
                elif condition_str.startswith("(:c_n_eq"): facts.append(("c_eq_fixed", [Number(r_idx), Number(f_idx + len(domain_feature_data.boolean_features))]))
                else:
                    raise Exception(f"Cannot parse condition {condition_str}")
            for effect in rule.get_effects():
                effect_str = effect.str()
                result = re.findall(r"\(.* (\d+)\)", effect_str)
                assert len(result) == 1
                f_idx = int(result[0])
                if effect_str.startswith("(:e_b_pos"):
                    facts.append(("e_pos_fixed", [Number(r_idx), Number(f_idx)]))
                    facts.append(("change", [Number(f_idx), Number(r_idx), Number(2)]))
                elif effect_str.startswith("(:e_b_neg"):
                    facts.append(("e_neg_fixed", [Number(r_idx), Number(f_idx)]))
                    facts.append(("change", [Number(f_idx), Number(r_idx), Number(1)]))
                elif effect_str.startswith("(:e_b_bot"):
                    facts.append(("e_bot_fixed", [Number(r_idx), Number(f_idx)]))
                    facts.append(("change", [Number(f_idx), Number(r_idx), Number(0)]))
                elif effect_str.startswith("(:e_n_inc"):
                    facts.append(("e_inc_fixed", [Number(r_idx), Number(f_idx + len(domain_feature_data.boolean_features))]))
                    facts.append(("change", [Number(f_idx + len(domain_feature_data.boolean_features)), Number(r_idx), Number(2)]))
                elif effect_str.startswith("(:e_n_dec"):
                    facts.append(("e_dec_fixed", [Number(r_idx), Number(f_idx + len(domain_feature_data.boolean_features))]))
                    facts.append(("change", [Number(f_idx + len(domain_feature_data.boolean_features)), Number(r_idx), Number(1)]))
                elif effect_str.startswith("(:e_n_bot"):
                    facts.append(("e_bot_fixed", [Number(r_idx), Number(f_idx + len(domain_feature_data.boolean_features))]))
                    facts.append(("change", [Number(f_idx + len(domain_feature_data.boolean_features)), Number(r_idx), Number(0)]))
                else:
                    raise Exception(f"Cannot parse effect {effect_str}")
        return facts