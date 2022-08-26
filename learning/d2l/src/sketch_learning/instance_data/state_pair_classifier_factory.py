import math

from collections import deque, defaultdict
from enum import Enum
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
        source_idx_to_state_pairs_2 = defaultdict(set)
        expanded_s_idxs = set()
        generated_s_idxs = set()

        # First pass to classify state pairs
        queue = deque()
        reachable = set()
        queue.append(transition_system.initial_s_idx)
        reachable.add(transition_system.initial_s_idx)
        # delta deadends are leafs with no delta optimal state pair.
        # They can be used to identify other delta deadends
        delta_deadends = set()
        while queue:
            source_idx = queue.popleft()
            source_goal_distance = goal_distances.get(source_idx, math.inf)
            has_delta_optimal_state_pair = False
            for state_pair in source_idx_to_state_pairs[source_idx]:
                target_idx = state_pair.target_idx
                target_goal_distance = goal_distances.get(target_idx, math.inf)
                state_pair_distance = state_pair.distance
                if self.delta * source_goal_distance < target_goal_distance + state_pair_distance:
                    state_pair_to_classification[state_pair] = StatePairClassification.NOT_DELTA_OPTIMAL
                else:
                    has_delta_optimal_state_pair = True
                    state_pair_to_classification[state_pair] = StatePairClassification.DELTA_OPTIMAL
                    if target_idx not in reachable:
                        queue.append(target_idx)
                    reachable.add(target_idx)
            if not has_delta_optimal_state_pair:
                delta_deadends.add(source_idx)
            else:
                expanded_s_idxs.add(source_idx)
                for state_pair in source_idx_to_state_pairs[source_idx]:
                    generated_s_idxs.add(state_pair.target_idx)
                    source_idx_to_state_pairs_2[source_idx].add(state_pair)
            generated_s_idxs.add(source_idx)
        return StatePairClassifier(self.delta, state_pair_to_classification, source_idx_to_state_pairs_2, list(expanded_s_idxs), list(generated_s_idxs))

        # Second pass to prune additional delta deadends
