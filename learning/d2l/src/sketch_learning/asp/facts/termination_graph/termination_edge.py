from ..fact import Fact


class TerminationEdge(Fact):
    """ Defines an edge in the termination graph. """
    def __init__(self, instance_idx, r_idx_source, r_idx_target):
        super().__init__("termination_edge")
        self.instance_idx = instance_idx
        self.r_idx_source = r_idx_source
        self.r_idx_target = r_idx_target

    def __str__(self):
        return f"{self.name}({self.instance_idx}, {self.r_idx_source}, {self.r_idx_target}).\n"
