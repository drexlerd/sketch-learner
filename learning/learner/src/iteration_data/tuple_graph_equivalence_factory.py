import math
from typing import List
from collections import defaultdict
from dataclasses import dataclass

from learner.src.domain_data.domain_data import DomainData
from learner.src.instance_data.instance_data import InstanceData
from learner.src.iteration_data.tuple_graph_equivalence import TupleGraphEquivalence


@dataclass
class TupleGraphEquivalenceFactoryStatistics:
    num_subgoal_tuples: int = 0
    num_single_rule_subgoal_tuples: int = 0
    num_multi_rule_subgoal_tuples: int = 0

    def print(self):
        print("TupleGraphEquivalenceFactoryStatistics:")
        print("    num_subgoal_tuples:", self.num_subgoal_tuples)
        print("    num_single_rule_subgoal_tuples:", self.num_single_rule_subgoal_tuples)
        print("    num_multi_rule_subgoal_tuples:", self.num_multi_rule_subgoal_tuples)

    def collect_statistics(self, tuple_graph_equivalence: TupleGraphEquivalence):
        self.num_subgoal_tuples += len(tuple_graph_equivalence.t_idx_to_r_idxs)
        self.num_single_rule_subgoal_tuples += len([t_idx for t_idx, r_idxs in tuple_graph_equivalence.t_idx_to_r_idxs.items() if len(r_idxs) == 1])
        self.num_multi_rule_subgoal_tuples += len([t_idx for t_idx, r_idxs in tuple_graph_equivalence.t_idx_to_r_idxs.items() if len(r_idxs) > 1])


class TupleGraphEquivalenceFactory:
    """ Computes mappings between subgoals and rules over F.
    """
    def __init__(self):
        self.statistics = TupleGraphEquivalenceFactoryStatistics()

    def make_tuple_graph_equivalences(self, domain_data: DomainData, instance_datas: List[InstanceData]):
        """ Computes information for all subgoal states, tuples and rules over F.
        """
        for instance_data in instance_datas:
            tuple_graph_equivalences = dict()
            for s_idx, tuple_graph in instance_data.tuple_graphs.items():
                if instance_data.is_deadend(s_idx):
                    continue
                state_pair_equivalence = instance_data.state_pair_equivalences[s_idx]
                # rule distances, deadend rule distances
                r_idx_to_deadend_distance = dict()
                for state_distance, s_prime_idxs in enumerate(tuple_graph.get_state_indices_by_distance()):
                    for s_prime_idx in s_prime_idxs:
                        r_idx = state_pair_equivalence.subgoal_state_to_r_idx[s_prime_idx]
                        if instance_data.is_deadend(s_prime_idx):
                            r_idx_to_deadend_distance[r_idx] = min(r_idx_to_deadend_distance.get(r_idx, math.inf), state_distance)
                t_idx_to_r_idxs = defaultdict(set)
                t_idx_to_distance = dict()
                for subgoal_distance, tuple_nodes in enumerate(tuple_graph.get_tuple_nodes_by_distance()):
                    for tuple_node in tuple_nodes:
                        t_idx = tuple_node.get_tuple_index()
                        r_idxs = set()
                        for s_prime_idx in tuple_node.get_state_indices():
                            r_idx = state_pair_equivalence.subgoal_state_to_r_idx[s_prime_idx]
                            r_idxs.add(r_idx)
                        t_idx_to_distance[t_idx] = subgoal_distance
                        t_idx_to_r_idxs[t_idx] = r_idxs
                tuple_graph_equivalence = TupleGraphEquivalence(t_idx_to_r_idxs, t_idx_to_distance, r_idx_to_deadend_distance)
                #tuple_graph_equivalence.print()
                tuple_graph_equivalences[s_idx] = tuple_graph_equivalence
                self.statistics.collect_statistics(tuple_graph_equivalence)
            instance_data.tuple_graph_equivalences = tuple_graph_equivalences
