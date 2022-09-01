import math

from collections import deque, defaultdict
from enum import Enum
from os import stat
from typing import List, Dict, Tuple

from .instance_data import InstanceData
from .state_pair import StatePair
from .state_pair_classifier import StatePairClassification, StatePairClassifier
from .tuple_graph import TupleGraph


class StatePairClassifierFactory:
    def __init__(self, delta=1.0):
        assert delta >= 1
        self.delta = delta

    def make_state_pair_classifier(self, instance_data: InstanceData, tuple_graphs: List[TupleGraph], reachable_from_init=False):
        transition_system = instance_data.transition_system
        _, goal_distances = transition_system.partition_states_by_distance(transition_system.goal_s_idxs, forward=False, stop_upon_goal=False)

        # Compute relevant state pairs
        state_pairs = []
        for tuple_graph in tuple_graphs:
            if tuple_graph is None: continue
            for distance, target_idxs in enumerate(tuple_graph.s_idxs_by_distance):
                for target_idx in target_idxs:
                    state_pairs.append(StatePair(tuple_graph.root_idx, target_idx, distance))
                    assert distance <= 1
        source_idx_to_state_pairs = defaultdict(set)
        for state_pair in state_pairs:
            source_idx_to_state_pairs[state_pair.source_idx].add(state_pair)

        # Classify state pairs
        state_pair_to_classification = dict()
        expanded_s_idxs = set()
        generated_s_idxs = set()
        delta_deadends = set()
        for state_pair in state_pairs:
            source_goal_distance = goal_distances.get(state_pair.source_idx, math.inf)
            target_goal_distance = goal_distances.get(state_pair.target_idx, math.inf)
            # self loops
            if state_pair.source_idx == state_pair.target_idx:
                state_pair_to_classification[state_pair] = StatePairClassification.NOT_DELTA_OPTIMAL
            # best case path over state pair is worse than delta optimal worse case cost of source
            elif self.delta * source_goal_distance < target_goal_distance + state_pair.distance:
                state_pair_to_classification[state_pair] = StatePairClassification.NOT_DELTA_OPTIMAL
                delta_deadends.add(state_pair.target_idx)
            else:
                state_pair_to_classification[state_pair] = StatePairClassification.DELTA_OPTIMAL
                expanded_s_idxs.add(state_pair.source_idx)
                generated_s_idxs.add(state_pair.source_idx)
                generated_s_idxs.add(state_pair.target_idx)

        # Filter state pairs
        if reachable_from_init:
            source_idx_to_state_pairs_2 = dict()
            queue = deque()
            state_pair_to_classification_2 = dict()
            expanded_s_idxs_2 = set()
            generated_s_idxs_2 = set()
            delta_deadends_2 = set()
            queue.append(transition_system.initial_s_idx)
            generated_s_idxs_2.add(transition_system.initial_s_idx)
            while queue:
                source_idx = queue.popleft()
                has_delta_optimal = not all([state_pair_to_classification[state_pair] == StatePairClassification.NOT_DELTA_OPTIMAL for state_pair in source_idx_to_state_pairs[source_idx] if state_pair.distance > 0])
                if has_delta_optimal:
                    source_idx_to_state_pairs_2[source_idx] = source_idx_to_state_pairs[source_idx]
                    for state_pair in source_idx_to_state_pairs[source_idx]:
                        state_pair_to_classification_2[state_pair] = state_pair_to_classification[state_pair]
                        expanded_s_idxs_2.add(source_idx)
                        if state_pair.target_idx not in generated_s_idxs_2:
                            generated_s_idxs_2.add(state_pair.target_idx)
                            if state_pair_to_classification[state_pair] == StatePairClassification.DELTA_OPTIMAL:
                                queue.append(state_pair.target_idx)
                else:
                    delta_deadends_2.add(source_idx)
            # Set modified versions
            source_idx_to_state_pairs = source_idx_to_state_pairs_2
            state_pair_to_classification = state_pair_to_classification_2
            expanded_s_idxs = expanded_s_idxs_2
            generated_s_idxs = generated_s_idxs_2
            delta_deadends = delta_deadends_2

        state_pair_classifier = StatePairClassifier(self.delta, state_pair_to_classification, source_idx_to_state_pairs, list(expanded_s_idxs), list(generated_s_idxs))
        return state_pair_classifier
