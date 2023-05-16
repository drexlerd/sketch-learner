from collections import OrderedDict


class Feature:
    def __init__(self, dlplan_feature, complexity):
        self.dlplan_feature = dlplan_feature
        self.complexity = complexity


class Features:
    def __init__(self):
        self.f_idx_to_feature = dict()
        self.f_repr_to_feature = OrderedDict()

    def add_feature(self, feature: Feature):
        """
        overwrites an existing feature
        """
        f_repr = feature.dlplan_feature.compute_repr()
        if f_repr not in self.f_repr_to_feature:
            self.f_idx_to_feature[feature.dlplan_feature.get_index()] = feature
            self.f_repr_to_feature[f_repr] = feature
        else:
            self.f_repr_to_feature[f_repr].complexity = feature.complexity


class DomainFeatureData:
    """ DomainFeatureData stores all novel Boolean and Numerical features for a set of dlplan states. """
    def __init__(self):
        self.boolean_features = Features()
        self.numerical_features = Features()

    def print(self):
        print("Domain feature data:")
        print(f"    Boolean features: {self.boolean_features}")
        print(f"    Numerical features: {self.numerical_features}")
