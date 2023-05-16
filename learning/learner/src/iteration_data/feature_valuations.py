from typing import Dict
from dataclasses import dataclass


@dataclass
class StateFeatureValuation:
    s_idx: int
    b_idx_to_val: Dict[int, bool]
    n_idx_to_val: Dict[int, int]


    def __str__(self):
        return str(self.s_idx) + ": " + str(self.b_idx_to_val) + " " + str(self.n_idx_to_val)
