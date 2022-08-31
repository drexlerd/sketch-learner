import math
from typing import List
from collections import defaultdict

from .state_pair_equivalence import StatePairEquivalence
from .tuple_graph_equivalence import TupleGraphEquivalence

from ..instance_data.instance_data import InstanceData
from ..instance_data.tuple_graph import TupleGraph
from ..instance_data.state_pair import StatePair


class TupleGraphEquivalenceFactory:
    def make_tuple_graph_equivalence_datas(self, instance_data: InstanceData, tuple_graphs: List[TupleGraph], state_pair_equivalence_data: StatePairEquivalence):
        tuple_graph_equivalences = []
        for tuple_graph in tuple_graphs:
            if tuple_graph is None:
                tuple_graph_equivalences.append(None)
                continue
            # rule distances, deadend rule distances
            r_idxs_by_distance = []
            r_idx_to_deadend_distance = dict()
            r_idx_to_distance = dict()
            #print("Root state")
            #print(instance_data.transition_system.s_idx_to_dlplan_state[tuple_graph.root_idx])
            for distance, layer in enumerate(tuple_graph.s_idxs_by_distance):
                r_idxs = set()
                for s_idx in layer:
                    r_idx = state_pair_equivalence_data.state_pair_to_r_idx[StatePair(tuple_graph.root_idx, s_idx, distance)]
                    r_idxs.add(r_idx)
                    if instance_data.transition_system.is_deadend(s_idx):
                        # the first time we write r_idx = d, d is smallest value.
                        #print(tuple_graph.root_idx, s_idx, distance, r_idx)
                        #print(instance_data.transition_system.s_idx_to_dlplan_state[s_idx])
                        r_idx_to_deadend_distance[r_idx] = min(r_idx_to_deadend_distance.get(r_idx, math.inf), distance)
                    r_idx_to_distance[r_idx] = min(r_idx_to_distance.get(r_idx, math.inf), distance)
                r_idxs_by_distance.append(r_idxs)
            #print()
            # map tuple to rules and vice versa
            t_idx_to_r_idxs = defaultdict(set)
            r_idx_to_t_idxs = defaultdict(set)
            for distance, t_idxs in enumerate(tuple_graph.t_idxs_by_distance):
                for t_idx in t_idxs:
                    for s_idx in tuple_graph.t_idx_to_s_idxs[t_idx]:
                        r_idx = state_pair_equivalence_data.state_pair_to_r_idx[StatePair(tuple_graph.root_idx, s_idx, distance)]
                        t_idx_to_r_idxs[t_idx].add(r_idx)
                        r_idx_to_t_idxs[r_idx].add(t_idx)
            tuple_graph_equivalences.append(TupleGraphEquivalence(r_idxs_by_distance, t_idx_to_r_idxs, r_idx_to_t_idxs, r_idx_to_deadend_distance, r_idx_to_distance))
        return tuple_graph_equivalences
