from clingo import String, Number

from ....iteration_data.feature_data import DomainFeatureData


class DomainFeatureDataFactFactory():
    def make_facts(self, domain_feature_data: DomainFeatureData):
        facts = []
        for f_idx, boolean in enumerate(domain_feature_data.boolean_features):
            facts.append(("boolean", [String(f"b{f_idx}")]))
            facts.append(("feature", [String(f"b{f_idx}")]))
            facts.append(("complexity", [String(f"b{f_idx}"), Number(boolean.compute_complexity())]))
        for f_idx, numerical in enumerate(domain_feature_data.numerical_features):
            facts.append(("numerical", [String(f"n{f_idx}")]))
            facts.append(("feature", [String(f"n{f_idx}")]))
            facts.append(("complexity", [String(f"n{f_idx}"), Number(numerical.compute_complexity())]))
        return facts
