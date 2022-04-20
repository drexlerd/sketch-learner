from ..fact import Fact


class Contain(Fact):
    """ Defines that a tuple contains a certain state. """
    def __init__(self, instance_idx, root_idx, t_idx, r_idx):
        super().__init__("contain")
        self.instance_idx = instance_idx
        self.root_idx = root_idx
        self.t_idx = t_idx
        self.r_idx = r_idx

    def __str__(self):
        return f"{self.name}({self.instance_idx}, {self.root_idx}, {self.t_idx}, {self.r_idx}).\n"
