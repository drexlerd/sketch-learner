from dataclasses import dataclass
from typing import List, Dict
from pathlib import Path

from dlplan.core import DenotationsCaches
from dlplan.state_space import StateSpace

from .tuple_graph import PerStateTupleGraphs

from ..domain_data.domain_data import DomainData
from ..iteration_data.feature_valuations import PerStateFeatureValuations
from ..iteration_data.state_pair_equivalence import PerStateStatePairEquivalences
from ..iteration_data.tuple_graph_equivalence import PerStateTupleGraphEquivalences


@dataclass
class InstanceData:
    id: int
    domain_data: DomainData
    denotations_caches: DenotationsCaches  # We use a cache for each instance such that we can ignore the instance index.
    instance_filepath: Path
    state_space: StateSpace = None
    complete_state_space: StateSpace = None
    state_index_to_representative_state_index: Dict[int, int] = None
    goal_distances: Dict[int, int] = None
    per_state_tuple_graphs: PerStateTupleGraphs = None

    initial_s_idxs: List[int] = None  # in cases we need multiple initial states
    per_state_feature_valuations: PerStateFeatureValuations = None
    per_state_state_pair_equivalences: PerStateStatePairEquivalences = None
    per_state_tuple_graph_equivalences: PerStateTupleGraphEquivalences = None

    def is_deadend(self, s_idx: int):
        return self.goal_distances.get(s_idx, None) is None

    def is_goal(self, s_idx: int):
        return s_idx in self.state_space.get_goal_state_indices()

    def is_alive(self, s_idx: int):
        return not self.is_goal(s_idx) and not self.is_deadend(s_idx)
