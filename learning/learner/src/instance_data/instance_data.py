from dataclasses import dataclass
from typing import List, Dict
from pathlib import Path

import pymimir as mm
import dlplan.core as dlplan_core
from dlplan.core import DenotationsCaches
from dlplan.state_space import StateSpace

from .tuple_graph import PerStateTupleGraphs

from ..domain_data.domain_data import DomainData
from ..iteration_data.feature_valuations import PerStateFeatureValuations
from ..iteration_data.state_pair_equivalence import PerStateStatePairEquivalences
from ..iteration_data.tuple_graph_equivalence import PerStateTupleGraphEquivalences


@dataclass
class InstanceData:
    idx: int
    domain_data: DomainData
    denotations_caches: DenotationsCaches  # We use a cache for each instance such that we can ignore the instance index.
    instance_filepath: Path
    global_faithful_abstraction: mm.GlobalFaithfulAbstraction
    mimir_state_space: mm.StateSpace
    dlplan_state_space: StateSpace
    concrete_s_idx_to_global_s_idx: Dict[int, int]
    initial_global_s_idxs: List[int]  # in cases we need multiple initial states

    per_state_tuple_graphs: PerStateTupleGraphs = None
    per_state_feature_valuations: PerStateFeatureValuations = None
    per_state_state_pair_equivalences: PerStateStatePairEquivalences = None
    per_state_tuple_graph_equivalences: PerStateTupleGraphEquivalences = None

    def is_deadend(self, s_idx: int):
        return s_idx in self.mimir_state_space.get_deadend_states()

    def is_goal(self, s_idx: int):
        return s_idx in self.mimir_state_space.get_goal_states()

    def is_alive(self, s_idx: int):
        return not self.is_goal(s_idx) and not self.is_deadend(s_idx)

class StateFinder:
    def __init__(self, domain_data: DomainData, instance_datas: List[InstanceData]):
        self.instance_idx_remap = domain_data.instance_idx_remap
        self.domain_data = domain_data
        self.faithful_abstractions = instance_datas[0].global_faithful_abstraction.get_abstractions()
        self.instance_datas = instance_datas

    def get_state_id_in_complete_state_space(self, global_state: mm.GlobalFaithfulAbstractState) -> int:
        new_instance_id = self.instance_idx_remap[global_state.get_abstraction_id()]
        faithful_abstraction = self.faithful_abstractions[global_state.get_abstraction_id()]
        abstract_state = faithful_abstraction.get_states()[global_state.get_abstract_state_id()]
        mimir_state = abstract_state.get_state()
        mimir_state_space = self.instance_datas[new_instance_id].mimir_state_space
        state_id = mimir_state_space.get_state_id(mimir_state)

        return state_id

    def get_dlplan_state(self, global_state: mm.GlobalFaithfulAbstractState) -> dlplan_core.State:
        state_id = self.get_state_id_in_complete_state_space(global_state)
        new_instance_id = self.instance_idx_remap[global_state.get_abstraction_id()]
        dlplan_state_space = self.instance_datas[new_instance_id].dlplan_state_space
        dlplan_state = dlplan_state_space.get_states()[state_id]

        return dlplan_state

    def get_mimir_state(self, global_state: mm.GlobalFaithfulAbstractState) -> mm.State:
        faithful_abstraction = self.faithful_abstractions[global_state.get_abstraction_id()]
        abstract_state = faithful_abstraction.get_states()[global_state.get_abstract_state_id()]
        mimir_state = abstract_state.get_state()

        return mimir_state

    def get_global_state(self, instance_id: int, mimir_state: mm.State):
        instance_data = self.instance_datas[instance_id]

        state_id = instance_data.mimir_state_space.get_state_id(mimir_state)
        global_state = instance_data.global_faithful_abstraction.get_states()[instance_data.concrete_s_idx_to_global_s_idx[state_id]]

        return global_state




