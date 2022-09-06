import math

from collections import defaultdict, deque
from typing import List


from .state_pair_classifier import StatePairClassifier
from .transition_system import TransitionSystem


class TransitionSystemFactory:
    def parse_transition_system(self, s_idx_to_dlplan_state, goals, forward_transitions, initial_s_idx=0):
        # Compute backward transitions and deadends
        backward_transitions = compute_inverse_transitions(forward_transitions)
        goal_distances = compute_goal_distances(s_idx_to_dlplan_state, goals, backward_transitions)
        deadends = compute_deadends(goal_distances)
        return TransitionSystem(initial_s_idx, s_idx_to_dlplan_state, forward_transitions, backward_transitions, deadends, goals)

def compute_goal_distances(s_idx_to_dlplan_state, goals, backward_transitions):
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

def compute_inverse_transitions(transitions):
    inverse_transitions = defaultdict(set)
    for source_idx, outgoing_transitions in transitions.items():
        for target_idx in outgoing_transitions:
            inverse_transitions[target_idx].add(source_idx)
    return inverse_transitions

def compute_deadends(goal_distances):
    deadend_s_idxs = set()
    for s_idx, distance in goal_distances.items():
        if distance == math.inf:
            deadend_s_idxs.add(s_idx)
    return deadend_s_idxs
