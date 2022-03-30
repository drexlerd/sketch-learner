from .fact import Fact


class Unsolvable(Fact):
    """ Defines that a state is solvable."""
    def __init__(self, instance_idx, s_idx):
        super().__init__("unsolvable")
        self.instance_idx = instance_idx
        self.s_idx = s_idx

    def __str__(self):
        return f"{self.name}({self.instance_idx}, {self.s_idx}).\n"
