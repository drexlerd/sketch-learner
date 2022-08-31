import dlplan
import math

from typing import Dict, List, MutableSet
from collections import defaultdict, deque, OrderedDict

class TransitionSystem:
    def __init__(self,
        initial_s_idx: int,
        s_idx_to_dlplan_state: Dict[int, dlplan.State],
        forward_transitions: Dict[int, List[int]],
        backward_transitions: Dict[int, List[int]],
        deadend_s_idxs: MutableSet[int],
        goal_s_idxs: MutableSet[int]):
        self.initial_s_idx = initial_s_idx
        self.s_idx_to_dlplan_state = s_idx_to_dlplan_state
        self.forward_transitions = forward_transitions
        self.backward_transitions = backward_transitions
        self.deadend_s_idxs = deadend_s_idxs
        self.goal_s_idxs = goal_s_idxs

    def get_num_states(self):
        return len(self.s_idx_to_dlplan_state.items())

    def is_initial(self, state_index: int):
        return state_index == self.initial_s_idx

    def is_deadend(self, state_index: int):
        return state_index in self.deadend_s_idxs

    def is_goal(self, state_index: int):
        return state_index in self.goal_s_idxs

    def is_alive(self, state_index: int):
        return not self.is_goal(state_index) and not self.is_deadend(state_index)

    def partition_states_by_distance(self, states: List[int], forward=True, stop_upon_goal: bool = False, stop_upon_initial: bool = False) -> List[List[int]]:
        """ Perform BFS to partition states by their distance. """
        assert not (forward and stop_upon_initial)
        assert not (not forward and stop_upon_goal)
        layers = OrderedDict()
        queue = deque()
        distances = dict()
        for state in states:
            queue.append(state)
            distances[state] = 0
        if forward:
            transitions = self.forward_transitions
        else:
            transitions = self.backward_transitions
        while queue:
            curr_idx = queue.popleft()
            curr_cost = distances[curr_idx]
            layer = layers.setdefault(curr_cost, set())
            layer.add(curr_idx)
            if stop_upon_goal and self.is_goal(curr_idx): continue
            if stop_upon_initial and self.is_initial(curr_idx): continue
            for succ_idx in transitions[curr_idx]:
                succ_cost = distances.get(succ_idx, math.inf)
                if curr_cost + 1 < succ_cost:
                    if succ_idx not in distances:
                        queue.append(succ_idx)
                    distances[succ_idx] = curr_cost + 1
        return [list(l) for l in layers.values()], distances

    def print_statistics(self):
        print(f"Num states: {len(self.s_idx_to_dlplan_state)}")
        print(f"Num transitions: {sum([len(transitions) for transitions in self.forward_transitions.values()])}")
        print(f"Num deadends: {len(self.deadend_s_idxs)}")
        print(f"Num goals: {len(self.goal_s_idxs)}")
