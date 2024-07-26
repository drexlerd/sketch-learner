from typing import List

import pymimir as mm
import dlplan.core as dlplan_core

from .domain_data import DomainData
from .instance_data import InstanceData


class StateFinder:
    def __init__(self, domain_data: DomainData, instance_datas: List[InstanceData]):
        self.domain_data = domain_data
        self.instance_datas = instance_datas

        # Prefetching for efficiency
        self.gfa_states_by_instance_idx = [instance_data.gfa.get_states() for instance_data in instance_datas]
        self.fa_states_by_instance_idx = [fa.get_states() for fa in self.instance_datas[0].gfa.get_abstractions()]
        self.dlplan_ss_states_by_instance_id = [instance_data.dlplan_ss.get_states() for instance_data in instance_datas]

    def get_ss_state_idx(self, gfa_state: mm.GlobalFaithfulAbstractState) -> int:
        """ Get the index of the representative state in the complete concrete state space.
        """
        instance_idx = gfa_state.get_faithful_abstraction_index()
        fa_state = self.fa_states_by_instance_idx[instance_idx][gfa_state.get_faithful_abstract_state_index()]
        mimir_ss_state = fa_state.get_representative_state()
        mimir_ss = self.instance_datas[instance_idx].mimir_ss
        ss_state_idx = mimir_ss.get_state_index(mimir_ss_state)

        return ss_state_idx

    def get_dlplan_ss_state(self, gfa_state: mm.GlobalFaithfulAbstractState) -> dlplan_core.State:
        """ Get the representative dlplan state in the complete concrete dlplan state space.
        """
        ss_state_idx = self.get_ss_state_idx(gfa_state)
        dlplan_ss_state = self.dlplan_ss_states_by_instance_id[gfa_state.get_faithful_abstraction_index()][ss_state_idx]

        return dlplan_ss_state

    def get_mimir_ss_state(self, gfa_state: mm.GlobalFaithfulAbstractState) -> mm.State:
        """ Get the representative mimir state in the complete concrete mimir state space.
        """
        fa_state = self.fa_states_by_instance_idx[gfa_state.get_faithful_abstraction_index()][gfa_state.get_faithful_abstract_state_index()]
        mimir_ss_state = fa_state.get_representative_state()

        return mimir_ss_state

    def get_gfa_state_from_ss_state_idx(self, instance_idx: int, ss_state_idx: int):
        """ Get the global faithful abstract state of a state index from a complete concrete mimir state space.
        """
        instance_data = self.instance_datas[instance_idx]
        gfa_state = self.gfa_states_by_instance_idx[instance_idx][instance_data.ss_state_idx_to_gfa_state_idx[ss_state_idx]]

        return gfa_state