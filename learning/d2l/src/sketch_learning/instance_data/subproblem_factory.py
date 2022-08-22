import dlplan
import math

from collections import defaultdict, deque
from typing import List, MutableSet

from .subproblem import Transition, SubproblemData
from .instance_data import InstanceData

from ..iteration_data.sketch import SketchRule


class SubproblemDataFactory:
    def make_subproblems(self, instance_datas: List[InstanceData], rule: SketchRule):
        subproblem_datas = []
        for instance_data in instance_datas:
            for root_idx in range(instance_data.transition_system.get_num_states()):
                subproblem_data = self.make_subproblem(instance_data, rule, root_idx, len(subproblem_datas))
                if subproblem_data is not None:
                    subproblem_datas.append(subproblem_data)
        # sort by number of generated states and fix the broken indexing scheme
        sorted(subproblem_datas, key=lambda x : len(x.generated_states))
        for subproblem_idx, subproblem_data in enumerate(subproblem_datas):
            subproblem_data.id = subproblem_idx
        return subproblem_datas

    def make_subproblem(self, instance_data: InstanceData, rule: SketchRule, root_idx: int, subproblem_idx: int):
        if not instance_data.transition_system.is_alive(root_idx):
            return None
        closest_subgoal_states = self._compute_closest_subgoal_states(instance_data, root_idx, rule)
        if not closest_subgoal_states:
            return None
        expanded_states, generated_states, forward_transitions = self._compute_transitions_to_closest_subgoal_states(instance_data, root_idx, closest_subgoal_states)
        return SubproblemData(subproblem_idx, instance_data, root_idx, forward_transitions, expanded_states, generated_states, closest_subgoal_states)

    def _compute_closest_subgoal_states(self, instance_data: InstanceData, root_idx: int, rule: SketchRule):
        evaluation_cache = dlplan.EvaluationCache(len(rule.sketch.dlplan_policy.get_boolean_features()), len(rule.sketch.dlplan_policy.get_numerical_features()))
        root_context = dlplan.EvaluationContext(root_idx, instance_data.transition_system.states_by_index[root_idx], evaluation_cache)
        if not rule.dlplan_rule.evaluate_conditions(root_context):
            return set()
        layers, _ = instance_data.transition_system.partition_states_by_distance(states=[root_idx], forward=True, stop_upon_goal=False)
        for layer in layers:
            closest_subgoal_states = set()
            for target_idx in layer:
                target_context = dlplan.EvaluationContext(target_idx, instance_data.transition_system.states_by_index[target_idx], evaluation_cache)
                if rule.dlplan_rule.evaluate_effects(root_context, target_context):
                    closest_subgoal_states.add(target_idx)
            if closest_subgoal_states:
                return closest_subgoal_states
        return set()

    def _compute_transitions_to_closest_subgoal_states(self, instance_data: InstanceData, root_idx: int, closest_subgoal_states: MutableSet[int]):
        """ Compute set of transitions starting at states reached optimally from the initial states. """
        # 1. backward from subgoal states: compute optimal/not optimal transitions
        state_layers, distances = instance_data.transition_system.partition_states_by_distance(states=list(closest_subgoal_states), forward=False, stop_upon_goal=False)
        forward_transitions = defaultdict(set)
        for source_idx, target_idxs in instance_data.transition_system.forward_transitions.items():
            source_cost = distances.get(source_idx, math.inf)
            for target_idx in target_idxs:
                target_cost = distances.get(target_idx, math.inf)
                if source_cost == target_cost + 1:
                    forward_transitions[source_idx].add(Transition(source_idx, target_idx, True))
                else:
                    forward_transitions[source_idx].add(Transition(source_idx, target_idx, False))
        # 2. forward from initial state: move along optimal transitions and collect them, and also collect not optimal 1-step transitions.
        queue = deque()
        expanded_states = set()
        generated_states = set()
        relevant_forward_transitions = defaultdict(set)
        assert instance_data.transition_system.is_alive(root_idx)
        queue.append(root_idx)
        generated_states.add(root_idx)
        while queue:
            source_idx = queue.popleft()
            if source_idx in closest_subgoal_states:
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
