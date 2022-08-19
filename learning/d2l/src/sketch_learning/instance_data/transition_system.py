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

    def compute_distances_to_states(self, states: List[int]) -> Dict[int, int]:
        queue = deque()
        distances = dict()
        for target_idx in states:
            queue.append(target_idx)
            distances[target_idx] = 0
        while queue:
            target_idx = queue.popleft()
            target_cost = distances[target_idx]
            for source_idx in self.backward_transitions[target_idx]:
                source_cost = distances.get(source_idx, math.inf)
                if target_cost + 1 < source_cost:
                    queue.append(source_idx)
                    distances[source_idx] = target_cost + 1
        return distances

    def compute_states_by_distance(self, source: int):
        """ Perform BFS to partition states layerwise. """
        layers = OrderedDict()
        queue = deque()
        queue.append(source)
        distances = dict()
        distances[source] = 0
        while queue:
            curr_idx = queue.popleft()
            curr_cost = distances[curr_idx]
            layer = layers.setdefault(curr_cost, set())
            layer.add(curr_idx)
            # Stop upon reaching a goal:
            # Notice that we cannot stop upon reaching an deadend state since
            # those states contribute to novelty of states on goal paths.
            if curr_idx in self.goals: continue
            for succ_idx in self.forward_transitions[curr_idx]:
                succ_cost = distances.get(succ_idx, math.inf)
                if curr_cost + 1 < succ_cost:
                    if succ_idx not in distances:
                        queue.append(succ_idx)
                    distances[succ_idx] = curr_cost + 1
        return [list(l) for l in layers.values()]

    def compute_optimal_transitions_to_states(self, target_idxs: List[int]):
        distances = dict()
        queue = deque()
        for target_idx in target_idxs:
            distances[target_idx] = 0
            queue.append(target_idx)
        optimal_forward_transitions = defaultdict(set)
        optimal_backward_transitions = defaultdict(set)
        while queue:
            target_idx = queue.popleft()
            target_cost = distances.get(target_idx)
            for source_idx in self.backward_transitions[target_idx]:
                alt_distance = target_cost + 1
                if alt_distance < distances.get(source_idx, math.inf):
                    distances[source_idx] = alt_distance
                    queue.append(source_idx)
                if alt_distance == distances.get(source_idx):
                    optimal_forward_transitions[source_idx].add(target_idx)
                    optimal_backward_transitions[target_idx].add(source_idx)
        return optimal_forward_transitions, optimal_backward_transitions

    def print_statistics(self):
        print(f"Num states: {len(self.states_by_index)}")
        print(f"Num transitions: {sum([len(transitions) for transitions in self.forward_transitions.values()])}")
        print(f"Num deadends: {len(self.deadends)}")
        print(f"Num goals: {len(self.goals)}")
