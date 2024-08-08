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
    _mimir_ss: mm.StateSpace
    _dlplan_ss: dlplan_state_space.StateSpace
    _initial_ss_state_idxs: List[int]  # in cases we need multiple initial states

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
    def mimir_ss(self):
        return self._mimir_ss

    @property
    def dlplan_ss(self):
        return self._dlplan_ss

    @property
    def initial_ss_state_idxs(self):
        return self._initial_ss_state_idxs
