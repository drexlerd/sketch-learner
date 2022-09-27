import dlplan
from typing import Dict, List, MutableSet
from dataclasses import dataclass
from .feature_valuations import FeatureValuation


@dataclass
class InstanceStateEquivalence:
    """
    StateEquivalence maps state index to state equivalence class index.
    Two states s,s' are considered equivalent, i.e., s~s',
    iff f(s) = f(s') for all f in feature pool F.

    This creates an abstraction of the states that allows
    reducing the number of constraints in the propositonal encoding.
    """
    # mapping from state index to state equivalence class index.
    s_idx_to_state_class_idx: Dict[int, int]
    state_class_idx_to_s_idxs: Dict[int, MutableSet[int]]

    def print(self):
        print("StateEquivalence:")
        print("    s_idx_to_state_class_idx:", self.s_idx_to_state_class_idx)
        print("    state_class_idx_to_s_idxs:", self.state_class_idx_to_s_idxs)


@dataclass
class DomainStateEquivalence:
    # Indices 0,...,n-1 of n state classes
    feature_valuation_to_state_class_idx: Dict[FeatureValuation, int]
    # state classes where all states are goals
    goal_state_class_idxs: MutableSet[int]
    # state classes where all states are non goals
    nongoal_state_class_idxs: MutableSet[int]
    # state classes where there is at least one goal and one non goal state
    mixed_state_class_idxs: MutableSet[int]  # must be empty in case of goal separation

    def print(self):
        print("DomainStateEquivalence:")
        print("    feature_valuation_to_state_class_idx:", self.feature_valuation_to_state_class_idx)
        print("    goal_state_class_idxs:", self.goal_state_class_idxs)
        print("    nongoal_state_class_idxs:", self.nongoal_state_class_idxs)
        print("    mixed_state_class_idxs:", self.mixed_state_class_idxs)
