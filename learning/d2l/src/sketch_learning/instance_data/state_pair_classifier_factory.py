import math

from collections import deque, defaultdict

from .instance_data import InstanceData
from .state_pair import StatePair
from .state_pair_classifier import StatePairClassification, StatePairClassifier


class StatePairClassifierFactory:
    def __init__(self, delta=1.0):
        assert delta >= 1
        self.delta = delta

    def make_state_pair_classifier(self, config, instance_data: InstanceData):
        # Compute relevant state pairs
        state_pairs = []
        state_pair_to_distance = dict()
        source_idx_to_state_pairs = defaultdict(set)
        target_idx_to_state_pairs = defaultdict(set)
        for s_idx in instance_data.state_space.get_state_indices():
            if not instance_data.goal_distance_information.is_alive(s_idx):
                continue
            assert instance_data.tuple_graphs[s_idx] is not None
            tuple_graph = instance_data.tuple_graphs[s_idx]
            for distance, target_idxs in enumerate(tuple_graph.s_idxs_by_distance):
                for target_idx in target_idxs:
                    state_pair = StatePair(tuple_graph.root_idx, target_idx)
                    state_pairs.append(state_pair)
                    state_pair_to_distance[state_pair] = distance
                    source_idx_to_state_pairs[tuple_graph.root_idx].add(state_pair)
                    target_idx_to_state_pairs[target_idx].add(state_pair)
        # Classify state pairs
        state_pair_to_classification = dict()
        expanded_s_idxs = set()
        generated_s_idxs = set()
        goal_distances = instance_data.goal_distance_information.get_goal_distances()

        for state_pair in state_pairs:
            source_goal_distance = goal_distances.get(state_pair.source_idx, math.inf)
            target_goal_distance = goal_distances.get(state_pair.target_idx, math.inf)
            # what value will INF be?
            assert source_goal_distance != math.inf or source_goal_distance < 100000000
            assert source_goal_distance != math.inf or target_goal_distance < 100000000
            # self loops
            if state_pair.source_idx == state_pair.target_idx:
                state_pair_to_classification[state_pair] = StatePairClassification.NOT_DELTA_OPTIMAL
            # best case path over state pair is worse than delta optimal worse case cost of source
            elif self.delta * source_goal_distance < target_goal_distance + state_pair_to_distance[state_pair]:
                state_pair_to_classification[state_pair] = StatePairClassification.NOT_DELTA_OPTIMAL
            else:
                state_pair_to_classification[state_pair] = StatePairClassification.DELTA_OPTIMAL
                expanded_s_idxs.add(state_pair.source_idx)
                generated_s_idxs.add(state_pair.source_idx)
                generated_s_idxs.add(state_pair.target_idx)

        # Restrict to backward reachable parts
        # Every previous alive state remains alive
        # for all delta >= 1

        # Restrict to forward reachable parts
        if config.reachable_from_init:
            source_idx_to_state_pairs_2 = dict()
            state_pair_to_classification_2 = dict()
            expanded_s_idxs_2 = set()
            generated_s_idxs_2 = set()
            queue = deque()
            queue.append(instance_data.state_space.get_initial_state_index())
            generated_s_idxs_2.add(instance_data.state_space.get_initial_state_index())
            while queue:
                source_idx = queue.popleft()
                has_delta_optimal = not all([state_pair_to_classification[state_pair] == StatePairClassification.NOT_DELTA_OPTIMAL for state_pair in source_idx_to_state_pairs[source_idx] if state_pair_to_distance[state_pair] > 0])
                if has_delta_optimal:
                    source_idx_to_state_pairs_2[source_idx] = source_idx_to_state_pairs[source_idx]
                    for state_pair in source_idx_to_state_pairs[source_idx]:
                        state_pair_to_classification_2[state_pair] = state_pair_to_classification[state_pair]
                        expanded_s_idxs_2.add(source_idx)
                        if state_pair.target_idx not in generated_s_idxs_2:
                            generated_s_idxs_2.add(state_pair.target_idx)
                            if state_pair_to_classification[state_pair] == StatePairClassification.DELTA_OPTIMAL:
                                queue.append(state_pair.target_idx)
            # Set modified versions
            source_idx_to_state_pairs = source_idx_to_state_pairs_2
            state_pair_to_classification = state_pair_to_classification_2
            expanded_s_idxs = expanded_s_idxs_2
            generated_s_idxs = generated_s_idxs_2

        state_pair_classifier = StatePairClassifier(self.delta, state_pair_to_classification, state_pair_to_distance, source_idx_to_state_pairs, expanded_s_idxs, generated_s_idxs)
        return state_pair_classifier
