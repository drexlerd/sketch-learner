import dlplan
from typing import Dict, List, MutableSet, Tuple
from dataclasses import dataclass


@dataclass
class StatePairEquivalence:
    """
    InstanceStatePairEquivalence maps state pairs to rules over the feature pool F.

    This creates an abstraction of the state pairs that allows
    reducing the number of constraints in the propositonal encoding.
    """
    r_idx_to_subgoal_states: Dict[int, MutableSet[int]]
    r_idx_to_distance: Dict[int, int]
    subgoal_state_to_r_idx: Dict[int, int]

    def print(self):
        print("StatePairEquivalence:")
        print("    r_idx_to_subgoal_state: ", self.r_idx_to_subgoal_states)
        print("    r_idx_to_distance:", self.r_idx_to_distance)
        print("    subgoal_state_to_r_idx: ", self.subgoal_state_to_r_idx)

@dataclass
class DomainStatePairEquivalence:
    rules: List[dlplan.Rule]

    def print(self):
        print("DomainStatePairEquivalence:")
        print("\n".join([rule.compute_repr() for rule in self.rules]))
