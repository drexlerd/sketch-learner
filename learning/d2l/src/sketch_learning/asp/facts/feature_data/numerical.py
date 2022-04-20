from ..fact import Fact


class Numerical(Fact):
    """ Defines a numerical feature. """
    def __init__(self, f_idx):
        super().__init__("numerical")
        self.f_idx = f_idx

    def __str__(self):
        return f"{self.name}({self.f_idx}).\n"
