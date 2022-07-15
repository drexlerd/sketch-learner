from ....iteration_data.feature_data import DomainFeatureData


class DomainFeatureDataFactFactory():
    def make_facts(self, domain_feature_data: DomainFeatureData):
        facts = []
        for f_idx, boolean in enumerate(domain_feature_data.boolean_features):
            facts.append(f"boolean(b{f_idx}).")
            facts.append(f"feature(b{f_idx}).")
            facts.append(f"complexity(b{f_idx},{boolean.compute_complexity()}).")
        for f_idx, numerical in enumerate(domain_feature_data.numerical_features):
            facts.append(f"numerical(n{f_idx}).")
            facts.append(f"feature(n{f_idx}).")
            facts.append(f"complexity(n{f_idx},{boolean.compute_complexity()}).")
        return facts
