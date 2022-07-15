import re
from ....iteration_data.equivalence_data import EquivalenceData
from ....iteration_data.feature_data import DomainFeatureData


class EquivalenceDataFactFactory():
    def make_facts(self, equivalence_data: EquivalenceData, domain_feature_data: DomainFeatureData):
        facts = []
        for r_idx, rule in enumerate(equivalence_data.rules):
            facts.append(f"equivalence({r_idx}).")
            for condition in rule.get_conditions():
                condition_str = condition.str()
                result = re.findall(r"\(.* (\d+)\)", condition_str)
                assert len(result) == 1
                f_idx = int(result[0])
                if condition_str.startswith("(:c_b_pos"): facts.append(f"c_pos_fixed({r_idx},b{f_idx}).")
                elif condition_str.startswith("(:c_b_neg"): facts.append(f"c_neg_fixed({r_idx},b{f_idx}).")
                elif condition_str.startswith("(:c_n_gt"): facts.append(f"c_gt_fixed({r_idx},n{f_idx}).")
                elif condition_str.startswith("(:c_n_eq"): facts.append(f"c_eq_fixed({r_idx},n{f_idx}).")
                else:
                    raise Exception(f"Cannot parse condition {condition_str}")
            for effect in rule.get_effects():
                effect_str = effect.str()
                result = re.findall(r"\(.* (\d+)\)", effect_str)
                assert len(result) == 1
                f_idx = int(result[0])
                if effect_str.startswith("(:e_b_pos"): facts.append(f"e_pos_fixed({r_idx},b{f_idx}).")
                elif effect_str.startswith("(:e_b_neg"): facts.append(f"e_neg_fixed({r_idx},b{f_idx}).")
                elif effect_str.startswith("(:e_b_bot"): facts.append(f"e_bot_fixed({r_idx},b{f_idx}).")
                elif effect_str.startswith("(:e_n_inc"): facts.append(f"e_inc_fixed({r_idx},n{f_idx}).")
                elif effect_str.startswith("(:e_n_dec"): facts.append(f"e_dec_fixed({r_idx},n{f_idx}).")
                elif effect_str.startswith("(:e_n_bot"): facts.append(f"e_bot_fixed({r_idx},n{f_idx}).")
                else:
                    raise Exception(f"Cannot parse effect {effect_str}")
        return facts