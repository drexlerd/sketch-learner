import math

from collections import defaultdict, deque
from typing import List

from .transition_system import TransitionSystem


class TransitionSystemFactory:
    def parse_transition_system(self, s_idx_to_dlplan_state, goals, forward_transitions):
        # Compute backward transitions and deadends
        backward_transitions = compute_inverse_transitions(forward_transitions)
        goal_distances = self._compute_goal_distances(s_idx_to_dlplan_state, goals, backward_transitions)
        deadends = compute_deadends(goal_distances)
        return TransitionSystem(0, s_idx_to_dlplan_state, forward_transitions, backward_transitions, deadends, goals, goal_distances)

    def _normalize_atom_name(self, name):
        tmp = name.replace('()', '').replace(')', '').replace('(', ',')
        if "=" in tmp:  # We have a functional atom
            tmp = tmp.replace("=", ',')
        return tmp.split(',')

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


def compute_inverse_transitions(transitions):
    inverse_transitions = defaultdict(set)
    for source_idx, outgoing_transitions in transitions.items():
        for target_idx in outgoing_transitions:
            inverse_transitions[target_idx].add(source_idx)
    return inverse_transitions


def compute_deadends(goal_distances):
    deadends = set()
    for state_idx, distance in enumerate(goal_distances):
        if distance == math.inf:
            deadends.add(state_idx)
    return deadends
