from typing import Dict, MutableSet
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class TupleGraphEquivalence:
    """
    TupleGraphEquivalence maps tuple information to rules over the feature pool F of a subproblem.

    This is necessary for constructing the constraints in the propositional encoding
    relevant to bound the width of the subproblem.
    """
    t_idx_to_r_idxs: Dict[int, MutableSet[int]] = field(default_factory=lambda: defaultdict(set))
    t_idx_to_distance: Dict[int, int] = field(default_factory=dict)
    r_idx_to_deadend_distance: Dict[int, int] = field(default_factory=dict)
