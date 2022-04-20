from ..fact import Fact


class Equivalence(Fact):
    """ Defines an rule over feature pool F. """
    def __init__(self, r_idx):
        super().__init__("equivalence")
        self.r_idx = r_idx

    def __str__(self):
        return f"{self.name}({self.r_idx}).\n"
