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
        s_idx_to_dlplan_state = dict()
        deadend_s_idxs = set()
        for s_idx in generated_s_idxs:
            s_idx_to_dlplan_state[s_idx] = transition_system.s_idx_to_dlplan_state[s_idx]
            if s_idx in transition_system.deadend_s_idxs:
                deadend_s_idxs.add(s_idx)
        forward_transitions = defaultdict(set)
        backward_transitions = defaultdict(set)
        for source_idx, target_idxs in transition_system.forward_transitions.items():
            if source_idx not in generated_s_idxs:
                continue
            for target_idx in target_idxs:
                if target_idx not in generated_s_idxs:
                    continue
                forward_transitions[source_idx].add(target_idx)
                backward_transitions[target_idx].add(source_idx)
        assert transition_system.initial_s_idx in generated_s_idxs
        return TransitionSystem(transition_system.initial_s_idx, s_idx_to_dlplan_state, forward_transitions, backward_transitions, deadend_s_idxs, transition_system.goal_s_idxs)

    def _compute_goal_distances(self, s_idx_to_dlplan_state, goals, backward_transitions):
        distances = [math.inf for _ in s_idx_to_dlplan_state]
        queue = deque()
        for goal in goals:
            distances[goal] = 0
            queue.append(goal)
        while queue:
            curr_idx = queue.popleft()
            curr_distance = distances[curr_idx]
            assert curr_distance != math.inf
            for succ_idx in backward_transitions.get(curr_idx, []):
                if distances[succ_idx] == math.inf:
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
        deadends = set()
        for state_idx, distance in enumerate(goal_distances):
            if distance == math.inf:
                deadends.add(state_idx)
        return deadends
