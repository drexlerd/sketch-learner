import dlplan
import math
from typing import Dict, List, MutableSet, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

from ..instance_data.instance_data import InstanceData

@dataclass
class StatePairData:
    state_pairs: List[Tuple[int, int]]


class StatePairDataFactory:
    def make_state_pairs_from_tuple_graphs(self, instance_datas: List[InstanceData]):
        instance_state_pair_datas = []
        for instance_data in instance_datas:
            state_pairs = []
            for tuple_graph in instance_data.tuple_graphs_by_state_index:
                if tuple_graph is None: continue
                for target_idxs in tuple_graph.s_idxs_by_distance:
                    for target_idx in target_idxs:
                        state_pairs.append((tuple_graph.root_idx, target_idx))
            instance_state_pair_datas.append(StatePairData(state_pairs))
        return instance_state_pair_datas