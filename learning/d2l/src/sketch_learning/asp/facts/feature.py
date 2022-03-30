from .fact import Fact


class Feature(Fact):
    """ Defines a feature. """
    def __init__(self, f_idx):
        super().__init__("feature")
        self.f_idx = f_idx

    def __str__(self):
        return f"{self.name}({self.f_idx}).\n"
