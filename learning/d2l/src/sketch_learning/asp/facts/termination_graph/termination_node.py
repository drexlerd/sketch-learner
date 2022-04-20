from ..fact import Fact


class TerminationNode(Fact):
    """ Defines a node in the termination graph. """
    def __init__(self, instance_idx, r_idx):
        super().__init__("termination_node")
        self.instance_idx = instance_idx
        self.r_idx = r_idx

    def __str__(self):
        return f"{self.name}({self.instance_idx}, {self.r_idx}).\n"
