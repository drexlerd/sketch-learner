from typing import Dict, List, MutableSet
from dataclasses import dataclass


@dataclass
class TupleGraphEquivalenceData:
    """
    TupleGraphEquivalenceData maps tuple information to rules over the feature pool F of a subproblem.

    This is necessary for constructing the constraints in the propositional encoding
    relevant to bound the width of the subproblem.
    """
    r_idxs_by_distance: List[MutableSet[int]]
    t_idx_to_r_idxs: Dict[int, MutableSet[int]]
    r_idx_to_t_idxs: Dict[int, MutableSet[int]]
    r_idx_to_deadend_distance: Dict[int, int]
    r_idx_to_distance: Dict[int, int]
