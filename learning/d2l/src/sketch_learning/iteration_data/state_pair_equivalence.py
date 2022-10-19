import dlplan
from typing import Dict, List, MutableSet, Tuple
from dataclasses import dataclass


@dataclass
class InstanceStatePairEquivalence:
    """
    InstanceStatePairEquivalence maps state pairs to rules over the feature pool F.

    This creates an abstraction of the state pairs that allows
    reducing the number of constraints in the propositonal encoding.
    """
    r_idx_to_state_pairs: Dict[int, MutableSet[Tuple[int, int]]]
    state_pair_to_r_idx: Dict[Tuple[int, int], int]

    def print(self):
        print("StatePairEquivalence:")
        print("    r_idx_to_state_pairs: ", self.r_idx_to_state_pairs)
        print("    state_pair_to_r_idx: ", self.state_pair_to_r_idx)

@dataclass
class DomainStatePairEquivalence:
    rules: List[dlplan.Rule]
