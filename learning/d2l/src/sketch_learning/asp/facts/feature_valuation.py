from .fact import Fact


class FeatureValuation(Fact):
    """ Defines the feature valuation in a given state. """
    def __init__(self, instance_idx, f_idx, s_idx, f_valuation):
        super().__init__("feature_valuation")
        self.instance_idx = instance_idx
        self.f_idx = f_idx
        self.s_idx = s_idx
        self.f_valuation = f_valuation
