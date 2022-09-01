import math

from collections import defaultdict, deque
from typing import List


from .state_pair_classifier import StatePairClassifier
from .transition_system import TransitionSystem


class TransitionSystemFactory:
    def parse_transition_system(self, s_idx_to_dlplan_state, goals, forward_transitions, initial_s_idx=0):
        # Compute backward transitions and deadends
        backward_transitions = self._compute_inverse_transitions(forward_transitions)
        goal_distances = self._compute_goal_distances(s_idx_to_dlplan_state, goals, backward_transitions)
        deadends = self._compute_deadends(goal_distances)
        return TransitionSystem(initial_s_idx, s_idx_to_dlplan_state, forward_transitions, backward_transitions, deadends, goals)

    def restrict_transition_system_by_state_classifier(self, transition_system: TransitionSystem, state_pair_classifier: StatePairClassifier) -> TransitionSystem:
        generated_s_idxs = set(state_pair_classifier.generated_s_idxs)
        expanded_s_idxs = set(state_pair_classifier.expanded_s_idxs)
        s_idx_to_dlplan_state = dict()
        for s_idx in generated_s_idxs:
            s_idx_to_dlplan_state[s_idx] = transition_system.s_idx_to_dlplan_state[s_idx]
        forward_transitions = defaultdict(set)
        backward_transitions = defaultdict(set)
        for source_idx, target_idxs in transition_system.forward_transitions.items():
            if source_idx not in expanded_s_idxs:
                continue
            for target_idx in target_idxs:
                forward_transitions[source_idx].add(target_idx)
                backward_transitions[target_idx].add(source_idx)
        goal_distances = self._compute_goal_distances(s_idx_to_dlplan_state, transition_system.goal_s_idxs, backward_transitions)
        deadend_s_idxs = self._compute_deadends(goal_distances)
        assert transition_system.initial_s_idx in generated_s_idxs
        return TransitionSystem(transition_system.initial_s_idx, s_idx_to_dlplan_state, forward_transitions, backward_transitions, deadend_s_idxs, transition_system.goal_s_idxs)

    def _compute_goal_distances(self, s_idx_to_dlplan_state, goals, backward_transitions):
        distances = dict()
        for s_idx in s_idx_to_dlplan_state.keys():
            distances[s_idx] = math.inf
        queue = deque()
        for goal in goals:
            distances[goal] = 0
            queue.append(goal)
        while queue:
            curr_idx = queue.popleft()
            curr_distance = distances.get(curr_idx, math.inf)
            assert curr_distance != math.inf
            for succ_idx in backward_transitions.get(curr_idx, []):
                succ_distance = distances.get(succ_idx, math.inf)
                if succ_distance == math.inf:
                    distances[succ_idx] = curr_distance + 1
                    queue.append(succ_idx)
        return distances

    def _compute_inverse_transitions(self, transitions):
        inverse_transitions = defaultdict(set)
        for source_idx, outgoing_transitions in transitions.items():
            for target_idx in outgoing_transitions:
                inverse_transitions[target_idx].add(source_idx)
        return inverse_transitions

    def _compute_deadends(self, goal_distances):
        deadend_s_idxs = set()
        for s_idx, distance in goal_distances.items():
            if distance == math.inf:
                deadend_s_idxs.add(s_idx)
        return deadend_s_idxs
