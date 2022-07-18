import dlplan
import math

from typing import List, MutableSet, Dict
from dataclasses import dataclass, field
from collections import defaultdict, OrderedDict, deque

from .return_codes import ReturnCode
from ..util.command import read_file

class TransitionSystem:
    def __init__(self,
        states_by_index: List[dlplan.State],
        forward_transitions: Dict[int, List[int]],
        backward_transitions: Dict[int, List[int]],
        deadends: MutableSet[int],
        goals: MutableSet[int],
        goal_distances: List[int]):
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

class TransitionSystemFactory:
    def __init__(self):
        pass

    def parse_transition_system(self, dlplan_states, goals, forward_transitions):
        # Compute backward transitions and deadends
        backward_transitions = compute_inverse_transitions(forward_transitions)
        goal_distances = self._compute_goal_distances(dlplan_states, goals, backward_transitions)
        deadends = compute_deadends(goal_distances)
        return TransitionSystem(dlplan_states, forward_transitions, backward_transitions, deadends, goals, goal_distances)

    def _normalize_atom_name(self, name):
        tmp = name.replace('()', '').replace(')', '').replace('(', ',')
        if "=" in tmp:  # We have a functional atom
            tmp = tmp.replace("=", ',')
        return tmp.split(',')


    def _compute_goal_distances(self, states_by_index, goals, backward_transitions):
        distances = [math.inf for _ in states_by_index]
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
