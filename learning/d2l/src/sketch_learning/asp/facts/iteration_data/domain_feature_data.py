from clingo import String, Number

from ....iteration_data.feature_data import DomainFeatureData


class DomainFeatureDataFactFactory():
    def make_facts(self, domain_feature_data: DomainFeatureData):
        facts = []
        for f_idx, boolean in enumerate(domain_feature_data.boolean_features):
            facts.append(("boolean", [Number(f_idx)]))
            facts.append(("feature", [Number(f_idx)]))
            facts.append(("complexity", [Number(f_idx), Number(boolean.compute_complexity())]))
        for f_idx, numerical in enumerate(domain_feature_data.numerical_features):
            facts.append(("numerical", [Number(f_idx + len(domain_feature_data.boolean_features))]))
            facts.append(("feature", [Number(f_idx + len(domain_feature_data.boolean_features))]))
            facts.append(("complexity", [Number(f_idx + len(domain_feature_data.boolean_features)), Number(numerical.compute_complexity())]))
        return facts
