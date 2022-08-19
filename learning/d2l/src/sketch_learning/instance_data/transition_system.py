import dlplan
import math

from typing import Dict, List, MutableSet
from collections import defaultdict, deque, OrderedDict


class TransitionSystem:
    def __init__(self,
        initial_state_index: int,
        states_by_index: List[dlplan.State],
        forward_transitions: Dict[int, List[int]],
        backward_transitions: Dict[int, List[int]],
        deadends: MutableSet[int],
        goals: MutableSet[int],
        goal_distances: List[int]):
        self.initial_state_index = initial_state_index
        self.states_by_index = states_by_index
        self.forward_transitions = forward_transitions
        self.backward_transitions = backward_transitions
        self.deadends = deadends
        self.goals = goals
        self.goal_distances = goal_distances

    def get_num_states(self):
        return len(self.states_by_index)

    def is_deadend(self, state_index: int):
        return state_index in self.deadends

    def is_goal(self, state_index: int):
        return state_index in self.goals

    def is_alive(self, state_index: int):
        return not self.is_goal(state_index) and not self.is_deadend(state_index)

    def partition_states_by_distance(self, states: List[int], stop_upon_goal: bool = False) -> List[List[int]]:
        """ Perform BFS to partition states by their distance. """
        layers = OrderedDict()
        queue = deque()
        distances = dict()
        for state in states:
            queue.append(state)
            distances[state] = 0
        while queue:
            curr_idx = queue.popleft()
            curr_cost = distances[curr_idx]
            layer = layers.setdefault(curr_cost, set())
            layer.add(curr_idx)
            if stop_upon_goal and self.is_goal(curr_idx): continue
            for succ_idx in self.forward_transitions[curr_idx]:
                succ_cost = distances.get(succ_idx, math.inf)
                if curr_cost + 1 < succ_cost:
                    if succ_idx not in distances:
                        queue.append(succ_idx)
                    distances[succ_idx] = curr_cost + 1
        return [list(l) for l in layers.values()], distances

    def print_statistics(self):
        print(f"Num states: {len(self.states_by_index)}")
        print(f"Num transitions: {sum([len(transitions) for transitions in self.forward_transitions.values()])}")
        print(f"Num deadends: {len(self.deadends)}")
        print(f"Num goals: {len(self.goals)}")
