import math
from .fact import Fact


class StateDistance(Fact):
    """ Defines the distance from source to target state. """
    def __init__(self, instance_idx, source_idx, target_idx, distance):
        super().__init__("s_distance")
        assert distance != math.inf
        self.instance_idx = instance_idx
        self.source_idx = source_idx
        self.target_idx = target_idx
        self.distance = distance

    def __str__(self):
        return f"{self.name}({self.instance_idx}, {self.source_idx}, {self.target_idx}, {self.distance}).\n"
