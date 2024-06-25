from dataclasses import dataclass
from typing import List, Dict
from pathlib import Path

import pymimir as mm
import dlplan.core as dlplan_core
import dlplan.state_space as dlplan_state_space


@dataclass
class InstanceData:
    """ Immutable data class. """
    _idx: int
    _denotations_caches: dlplan_core.DenotationsCaches  # We use a cache for each instance such that we can ignore the instance index.
    _instance_filepath: Path
    _gfa: mm.GlobalFaithfulAbstraction
    _mimir_ss: mm.StateSpace
    _dlplan_ss: dlplan_state_space.StateSpace
    _ss_state_idx_to_gfa_state_idx: Dict[int, int]
    _initial_gfa_state_idxs: List[int]  # in cases we need multiple initial states

    @property
    def idx(self):
        return self._idx

    @property
    def denotations_caches(self):
        return self._denotations_caches

    @property
    def instance_filepath(self):
        return self._instance_filepath

    @property
    def gfa(self):
        return self._gfa

    @property
    def mimir_ss(self):
        return self._mimir_ss

    @property
    def dlplan_ss(self):
        return self._dlplan_ss

    @property
    def ss_state_idx_to_gfa_state_idx(self):
        return self._ss_state_idx_to_gfa_state_idx

    @property
    def initial_gfa_state_idxs(self):
        return self._initial_gfa_state_idxs
