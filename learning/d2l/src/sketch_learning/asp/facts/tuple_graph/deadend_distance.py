from ..fact import Fact


class DeadendDistance(Fact):
    """ Defines the finite deadend distance of an equivalence class in subproblem. """
    def __init__(self, instance_idx, root_idx, r_idx, distance):
        super().__init__("d_distance")
        self.instance_idx = instance_idx
        self.root_idx = root_idx
        self.r_idx = r_idx
        self.distance = distance

    def __str__(self):
        return f"{self.name}({self.instance_idx}, {self.root_idx}, {self.r_idx}, {self.distance}).\n"
