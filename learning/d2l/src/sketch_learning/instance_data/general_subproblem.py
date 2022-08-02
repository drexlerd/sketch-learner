from collections import defaultdict
from re import sub
import dlplan
import math

from typing import Dict, List, MutableSet, Tuple
from dataclasses import dataclass, field

from collections import deque

from .instance_data import InstanceData

@dataclass
class Transition:
    source_idx: int
    target_idx: int
    optimal: bool

    def __eq__(self, other):
        return self.source_idx == other.source_idx and self.target_idx == other.target_idx and self.optimal == other.optimal

    def __hash__(self):
        return hash((self.source_idx, self.target_idx, self.optimal))


@dataclass
class GeneralSubproblem:
    instance_data: InstanceData
    forward_transitions: Dict[int, List[MutableSet[Transition]]]  # there can be disjunctive sets of optimal transitions for a state
    expanded_states: MutableSet[int]
    generated_states: MutableSet[int]

    def print(self):
        print("Generalized subproblem:")
        print(f"    Forward transitions: {self.forward_transitions}")
        print(f"    Expanded states: {self.expanded_states}")
        print(f"    Generated states: {self.generated_states}")


class GeneralSubproblemFactory:
    def make_generalized_subproblems(self, instance_data: InstanceData, sketch: dlplan.Policy, rule: dlplan.Rule):
        for s_idx, state in enumerate(instance_data.transition_system.states_by_index):
            print(s_idx, str(state))
        for root_idx in range(instance_data.transition_system.get_num_states()):
            if instance_data.tuple_graphs_by_state_index[root_idx] is None: continue
            subgoal_states = self._compute_subgoal_states_in_generalized_subproblem(instance_data, root_idx, sketch, rule)
            print(subgoal_states)
            expanded_states, generated_states, relevant_forward_transitions = self._compute_transitions_in_generalized_subproblem(instance_data, root_idx, subgoal_states)
            print(relevant_forward_transitions)
        return []

    def _compute_subgoal_states_in_generalized_subproblem(self, instance_data: InstanceData, root_idx: int, sketch: dlplan.Policy, rule: dlplan.Rule, include_closer=False):
        """ Compute the closest subgoal states that bound the width. """
        evaluation_cache = dlplan.EvaluationCache(len(sketch.get_boolean_features()), len(sketch.get_numerical_features()))
        root_context = dlplan.EvaluationContext(root_idx, instance_data.transition_system.states_by_index[root_idx], evaluation_cache)
        tuple_graph = instance_data.tuple_graphs_by_state_index[root_idx]
        bounded = False
        closest_subgoal_states = set()
        for t_idxs in tuple_graph.t_idxs_by_distance:
            if not include_closer:
                closest_subgoal_states = set()
            for t_idx in t_idxs:
                is_subgoal_tuple = True
                for s_idx in tuple_graph.t_idx_to_s_idxs[t_idx]:
                    target_context = dlplan.EvaluationContext(s_idx, instance_data.transition_system.states_by_index[s_idx], evaluation_cache)
                    if instance_data.transition_system.is_goal(s_idx) or \
                        (rule.evaluate_conditions(root_context) and
                         rule.evaluate_effects(root_context, target_context)):
                        closest_subgoal_states.add(s_idx)
                    else:
                        is_subgoal_tuple = False
                if is_subgoal_tuple:
                    bounded = True
            if bounded:
                break
        if not bounded:
            raise Exception("Width of subproblem is not bounded correctly.")
        return closest_subgoal_states

    def _compute_transitions_in_generalized_subproblem(self, instance_data: InstanceData, initial_state: int, subgoal_states: MutableSet[int]):
        """ Compute set of transitions starting at states reached optimally from the initial states. """
        # 1. backward from subgoal states: compute optimal/not optimal transitions
        queue = deque()
        distances = dict()
        forward_transitions = defaultdict(set)
        for target_idx in subgoal_states:
            queue.append(target_idx)
            distances[target_idx] = 0
        while queue:
            target_idx = queue.popleft()
            target_cost = distances[target_idx]
            for source_idx in instance_data.transition_system.backward_transitions[target_idx]:
                source_cost = distances.get(source_idx, math.inf)
                if target_cost + 1 < source_cost:
                    queue.append(source_idx)
                    distances[source_idx] = target_cost + 1
                if distances[source_idx] == distances[target_idx] + 1:
                    forward_transitions[source_idx].add(Transition(source_idx, target_idx, True))
                else:
                    forward_transitions[source_idx].add(Transition(source_idx, target_idx, False))
        # 2. forward from initial state: move along optimal transitions and collect them, and also collect not optimal 1-step transitions.
        queue = deque()
        expanded_states = set()
        generated_states = set()
        relevant_forward_transitions = defaultdict(set)
        assert instance_data.transition_system.is_alive(initial_state)
        queue.append(initial_state)
        generated_states.add(initial_state)
        while queue:
            source_idx = queue.popleft()
            if source_idx in subgoal_states:
                continue
            expanded_states.add(source_idx)
            relevant_forward_transitions[source_idx] = forward_transitions[source_idx]
            for transition in forward_transitions[source_idx]:
                target_idx = transition.target_idx
                # only follow optimal transitions
                if transition.optimal and target_idx not in generated_states:
                    queue.append(target_idx)
                generated_states.add(target_idx)
        return expanded_states, generated_states, relevant_forward_transitions
