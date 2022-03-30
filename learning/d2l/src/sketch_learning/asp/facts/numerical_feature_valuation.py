from .fact import Fact


class NumericalFeatureValuation(Fact):
    """ Defines the feature valuation in a given state. """
    def __init__(self, instance_idx, f_idx, s_idx, f_valuation):
        super().__init__("feature_valuation")
        self.instance_idx = instance_idx
        self.f_idx = f_idx
        self.s_idx = s_idx
        self.f_valuation = f_valuation

    def __str__(self):
        return f"{self.name}({self.f_idx}, {self.instance_idx}, {self.s_idx}, {int(self.f_valuation)}).\n"
