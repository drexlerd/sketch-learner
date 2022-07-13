from .fact import Fact


class NumericalFeature(Fact):
    """ Defines a numerical feature. """
    def __init__(self, f_idx):
        self.f_idx = f_idx

    def __str__(self):
        return f"\
numerical(n{self.idx}).\n\
feature(n{self.idx}).\n\
complexity(n{self.idx},{self.complexity}.\n"
