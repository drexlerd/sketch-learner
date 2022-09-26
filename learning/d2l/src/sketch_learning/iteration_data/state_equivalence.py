import dlplan
from typing import Dict, List, MutableSet, Tuple
from dataclasses import dataclass


@dataclass
class StatePairEquivalence:
    """
    StateEquivalence maps state index to state equivalence class index.
    Two states s,s' are considered equivalent, i.e., s~s',
    iff f(s) = f(s') for all f in feature pool F.

    This creates an abstraction of the states that allows
    reducing the number of constraints in the propositonal encoding.
    """
    # mapping from state index to state equivalence class index.
    s_idx_to_se_idx: Dict[int, int]

    def print(self):
        print("StateEquivalence:")
        print("    s_idx_to_se_idx: ", self.s_idx_to_se_idx)


@dataclass
class RuleEquivalences:
    rules: List[dlplan.Rule]
