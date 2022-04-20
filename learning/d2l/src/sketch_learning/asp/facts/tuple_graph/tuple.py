from ..fact import Fact

class Tuple(Fact):
    """ Defines all the tuples that are part of the tuple graph for a given state. """
    def __init__(self, instance_idx, root_idx, t_idx):
        super().__init__("tuple")
        self.instance_idx = instance_idx
        self.root_idx = root_idx
        self.t_idx = t_idx

    def __str__(self):
        return f"{self.name}({self.instance_idx}, {self.root_idx}, {self.t_idx}).\n"
