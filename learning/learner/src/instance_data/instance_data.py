from dataclasses import dataclass
from typing import List, Dict
from pathlib import Path

import pymimir as mm
import dlplan.core as dlplan_core
from dlplan.core import DenotationsCaches
from dlplan.state_space import StateSpace

from ..domain_data.domain_data import DomainData


@dataclass
class InstanceData:
    # Persistent data
    idx: int
    domain_data: DomainData
    denotations_caches: DenotationsCaches  # We use a cache for each instance such that we can ignore the instance index.
    instance_filepath: Path
    gfa: mm.GlobalFaithfulAbstraction
    mimir_ss: mm.StateSpace
    dlplan_ss: StateSpace
    ss_state_idx_to_gfa_state_idx: Dict[int, int]
    initial_gfa_state_idxs: List[int]  # in cases we need multiple initial states

class StateFinder:
    def __init__(self, domain_data: DomainData, instance_datas: List[InstanceData]):
        self.domain_data = domain_data
        self.instance_datas = instance_datas

    def get_ss_state_idx(self, gfa_state: mm.GlobalFaithfulAbstractState) -> int:
        """ Get the index of the representative state in the complete concrete state space.
        """
        instance_idx = gfa_state.get_abstraction_id()
        fa = self.instance_datas[0].gfa.get_abstractions()[gfa_state.get_abstraction_id()]
        fa_state = fa.get_states()[gfa_state.get_abstract_state_id()]
        mimir_s = fa_state.get_state()
        mimir_ss = self.instance_datas[instance_idx].mimir_ss
        ss_state_idx = mimir_ss.get_state_index(mimir_s)

        return ss_state_idx

    def get_dlplan_ss_state(self, gfa_state: mm.GlobalFaithfulAbstractState) -> dlplan_core.State:
        """ Get the representative dlplan state in the complete concrete dlplan state space.
        """
        instance_idx = gfa_state.get_abstraction_id()
        ss_state_idx = self.get_ss_state_idx(gfa_state)
        dlplan_ss = self.instance_datas[instance_idx].dlplan_ss
        dlplan_ss_state = dlplan_ss.get_states()[ss_state_idx]

        return dlplan_ss_state

    def get_mimir_ss_state(self, gfa_state: mm.GlobalFaithfulAbstractState) -> mm.State:
        """ Get the representative mimir state in the complete concrete mimir state space.
        """
        fa = self.instance_datas[0].gfa.get_abstractions()[gfa_state.get_abstraction_id()]
        fa_state = fa.get_states()[gfa_state.get_abstract_state_id()]
        mimir_ss_state = fa_state.get_state()

        return mimir_ss_state

    def get_gfa_state(self, instance_idx: int, ss_state: mm.State):
        """ Get the global faithful abstract state of a state from a complete concrete mimir state space.
        """
        instance_data = self.instance_datas[instance_idx]
        gfa_state_idx = instance_data.mimir_ss.get_state_index(ss_state)
        gfa_state = instance_data.gfa.get_states()[instance_data.ss_state_idx_to_gfa_state_idx[gfa_state_idx]]

        return gfa_state

    def get_gfa_state_from_ss_state_idx(self, instance_idx: int, ss_state_idx: int):
        """ Get the global faithful abstract state of a state index from a complete concrete mimir state space.
        """
        instance_data = self.instance_datas[instance_idx]
        gfa_state = instance_data.gfa.get_states()[instance_data.ss_state_idx_to_gfa_state_idx[ss_state_idx]]

        return gfa_state




