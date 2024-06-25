from typing import Dict, MutableSet
from dataclasses import dataclass


@dataclass
class StatePairEquivalence:
    """
    InstanceStatePairEquivalence maps state pairs to rules over the feature pool F.

    This creates an abstraction of the state pairs that allows
    reducing the number of constraints in the propositonal encoding.
    """
    _r_idx_to_subgoal_gfa_state_ids: Dict[int, MutableSet[int]]
    _r_idx_to_closest_subgoal_distance: Dict[int, int]
    _subgoal_gfa_state_id_to_r_idx: Dict[int, int]

    @property
    def r_idx_to_subgoal_gfa_state_ids(self):
        return self._r_idx_to_subgoal_gfa_state_ids

    @property
    def r_idx_to_closest_subgoal_distance(self):
        return self._r_idx_to_closest_subgoal_distance

    @property
    def subgoal_gfa_state_id_to_r_idx(self):
        return self._subgoal_gfa_state_id_to_r_idx
