from dlplan.policy import Rule

from typing import Dict, List, MutableSet
from dataclasses import dataclass, field


@dataclass
class StatePairEquivalence:
    """
    InstanceStatePairEquivalence maps state pairs to rules over the feature pool F.

    This creates an abstraction of the state pairs that allows
    reducing the number of constraints in the propositonal encoding.
    """
    _r_idx_to_subgoal_states: Dict[int, MutableSet[int]]
    _r_idx_to_distance: Dict[int, int]
    _subgoal_state_to_r_idx: Dict[int, int]

    @property
    def r_idx_to_subgoal_states(self):
        return self._r_idx_to_subgoal_states

    @property
    def r_idx_to_distance(self):
        return self._r_idx_to_distance

    @property
    def subgoal_state_to_r_idx(self):
        return self._subgoal_state_to_r_idx

    def __str__(self):
        return f"StatePairEquivalence(\
            r_idx_to_subgoal_state={self.r_idx_to_subgoal_states}, \
            r_idx_to_distance={self.r_idx_to_distance}, \
            subgoal_state_to_r_idx={self.subgoal_state_to_r_idx})"


@dataclass
class StatePairEquivalenceClasses:
    _rules: List[Rule]

    @property
    def rules(self):
        return self._rules

    def __str__(self):
        rules_str = ", ".join([repr(rule) for rule in self.rules])
        return f"StatePairEquivalenceClasses(rules=[{rules_str}])"


@dataclass
class PerStateStatePairEquivalences:
    s_idx_to_state_pair_equivalence: Dict[int, StatePairEquivalence] = field(default_factory=dict)
