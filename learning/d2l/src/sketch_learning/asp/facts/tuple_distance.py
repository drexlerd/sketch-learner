from .fact import Fact


class TupleDistance(Fact):
    """ Defines the distance of a tuple in a tuple graph from a root. """
    def __init__(self, instance_idx, root_idx, t_idx, distance):
        super().__init__("t_distance")
        self.instance_idx = instance_idx
        self.root_idx = root_idx
        self.t_idx = t_idx
        self.distance = distance

    def __str__(self):
        return f"{self.name}({self.instance_idx}, {self.root_idx}, {self.t_idx}, {self.distance}).\n"
