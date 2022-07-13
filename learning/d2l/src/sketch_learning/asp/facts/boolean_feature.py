from .fact import Fact


class BooleanFeature(Fact):
    """ Defines a boolean feature. """
    def __init__(self, idx, complexity):
        self.idx = idx
        self.complexity = complexity

    def __str__(self):
        return f"\
boolean(b{self.idx}).\n\
feature(b{self.idx}).\n\
complexity(b{self.idx},{self.complexity}.\n"
