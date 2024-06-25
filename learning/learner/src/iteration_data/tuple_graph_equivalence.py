from typing import Dict, MutableSet
from dataclasses import dataclass


@dataclass
class TupleGraphEquivalence:
    """
    TupleGraphEquivalence maps tuple information to rules over the feature pool F of a subproblem.

    This is necessary for constructing the constraints in the propositional encoding
    relevant to bound the width of the subproblem.
    """
    _t_idx_to_r_idxs: Dict[int, MutableSet[int]]
    _t_idx_to_distance: Dict[int, int]
    _r_idx_to_deadend_distance: Dict[int, int]

    @property
    def t_idx_to_r_idxs(self):
        return self._t_idx_to_r_idxs

    @property
    def t_idx_to_distance(self):
        return self._t_idx_to_distance

    @property
    def r_idx_to_deadend_distance(self):
        return self._r_idx_to_deadend_distance
