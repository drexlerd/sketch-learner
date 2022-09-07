import dlplan
import math

from collections import deque, defaultdict
from typing import Dict, MutableSet


def compute_goal_distances(s_idx_to_dlplan_state: Dict[int, dlplan.State], goal_s_idxs: MutableSet[int], backward_transitions: Dict[int, MutableSet[int]]):
    distances = dict()
    for s_idx in s_idx_to_dlplan_state.keys():
        distances[s_idx] = math.inf
    queue = deque()
    for goal in goal_s_idxs:
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

def compute_inverse_transitions(transitions: Dict[int, MutableSet[int]]):
    inverse_transitions = defaultdict(set)
    for source_idx, outgoing_transitions in transitions.items():
        for target_idx in outgoing_transitions:
            inverse_transitions[target_idx].add(source_idx)
    return inverse_transitions

def compute_deadends(goal_distances: Dict[int, int]):
    deadend_s_idxs = set()
    for s_idx, distance in goal_distances.items():
        if distance == math.inf:
            deadend_s_idxs.add(s_idx)
    return deadend_s_idxs
