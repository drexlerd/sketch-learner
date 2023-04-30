from collections import OrderedDict


class Feature:
    def __init__(self, dlplan_feature, complexity):
        self.dlplan_feature = dlplan_feature
        self.complexity = complexity


class Features:
    def __init__(self):
        self.features_by_index = []
        self.features_by_repr = OrderedDict()

    def add_feature(self, feature: Feature):
        """
        overwrites an existing feature
        """
        feature_repr = feature.dlplan_feature.compute_repr()
        if feature_repr not in self.features_by_repr:
            self.features_by_index.append(feature)
            self.features_by_repr[feature_repr] = feature
        else:
            self.features_by_repr[feature_repr].complexity = feature.complexity


class DomainFeatureData:
    """ DomainFeatureData stores all novel Boolean and Numerical features for a set of dlplan states. """
    def __init__(self):
        self.boolean_features = Features()
        self.numerical_features = Features()

    def print(self):
        print("Domain feature data:")
        print(f"    Boolean features: {self.boolean_features}")
        print(f"    Numerical features: {self.numerical_features}")
