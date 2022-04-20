from ..fact import Fact


class Exceed(Fact):
    """ Defines that the width of a state exceeds the upper bound. """
    def __init__(self, instance_idx, s_idx):
        super().__init__("exceed")
        self.instance_idx = instance_idx
        self.s_idx = s_idx

    def __str__(self):
        return f"{self.name}({self.instance_idx}, {self.s_idx}).\n"
