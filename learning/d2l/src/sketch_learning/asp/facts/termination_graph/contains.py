from ..fact import Fact


class EquivalenceContains(Fact):
    """ Defines a state pair underlying equivalence class. """
    def __init__(self, instance_idx, r_idx, s_idx_from, s_idx_to):
        super().__init__("equivalence_contains")
        self.instance_idx = instance_idx
        self.r_idx = r_idx
        self.s_idx_from = s_idx_from
        self.s_idx_to = s_idx_to

    def __str__(self):
        return f"{self.name}({self.instance_idx}, {self.r_idx}, {self.s_idx_from}, {self.s_idx_to}).\n"
