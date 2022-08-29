import math

from collections import deque, defaultdict
from enum import Enum
from os import stat
from typing import List, Dict, Tuple

from .instance_data import InstanceData
from .state_pair import StatePair
from .state_pair_classifier import StatePairClassification, StatePairClassifier


class StatePairClassifierFactory:
    def __init__(self, delta=1.0):
        assert delta >= 1
        self.delta = delta

    def make_state_pair_classifier(self, instance_data: InstanceData, state_pairs: List[StatePair]):
        transition_system = instance_data.transition_system
        _, goal_distances = transition_system.partition_states_by_distance(instance_data.transition_system.goal_s_idxs, forward=False, stop_upon_goal=False)

        source_idx_to_state_pairs = defaultdict(set)
        for state_pair in state_pairs:
            source_idx_to_state_pairs[state_pair.source_idx].add(state_pair)

        state_pair_to_classification = dict()
        expanded_s_idxs = set()
        generated_s_idxs = set()
        delta_deadends = set()
        for state_pair in state_pairs:
            source_goal_distance = goal_distances.get(state_pair.source_idx, math.inf)
            target_goal_distance = goal_distances.get(state_pair.target_idx, math.inf)
            if self.delta * source_goal_distance < target_goal_distance + state_pair.distance:
                state_pair_to_classification[state_pair] = StatePairClassification.NOT_DELTA_OPTIMAL
                delta_deadends.add(state_pair.target_idx)
            else:
                state_pair_to_classification[state_pair] = StatePairClassification.DELTA_OPTIMAL
                expanded_s_idxs.add(state_pair.source_idx)
                generated_s_idxs.add(state_pair.source_idx)
                generated_s_idxs.add(state_pair.target_idx)
        return StatePairClassifier(self.delta, state_pair_to_classification, source_idx_to_state_pairs, list(expanded_s_idxs), list(generated_s_idxs))
