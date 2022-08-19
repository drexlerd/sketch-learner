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
                if not instance_data.transition_system.is_alive(root_idx):
                    continue
                closest_subgoal_states = self._compute_closest_subgoal_states(instance_data, root_idx, rule)
                if not closest_subgoal_states:
                    continue
                expanded_states, generated_states, forward_transitions = self._compute_transitions_to_closest_subgoal_states(instance_data, root_idx, closest_subgoal_states)
                subproblem_data = SubproblemData(len(subproblem_datas), instance_data, root_idx, forward_transitions, expanded_states, generated_states)
                subproblem_datas.append(subproblem_data)
        # sort by number of generated states and fix the broken indexing scheme
        sorted(subproblem_datas, key=lambda x : len(x.generated_states))
        for subproblem_idx, subproblem_data in enumerate(subproblem_datas):
            subproblem_data.id = subproblem_idx
        return subproblem_datas

    def _compute_closest_subgoal_states(self, instance_data: InstanceData, root_idx: int, rule: SketchRule):
        evaluation_cache = dlplan.EvaluationCache(len(rule.sketch.dlplan_policy.get_boolean_features()), len(rule.sketch.dlplan_policy.get_numerical_features()))
        root_context = dlplan.EvaluationContext(root_idx, instance_data.transition_system.states_by_index[root_idx], evaluation_cache)
        if not rule.dlplan_rule.evaluate_conditions(root_context):
            return set()
        layers = instance_data.transition_system.compute_states_by_distance(root_idx)
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
        distances = instance_data.transition_system.compute_distances_to_states(closest_subgoal_states)
        forward_transitions = defaultdict(set)
        for source_idx, target_idxs in instance_data.transition_system.forward_transitions.items():
            for target_idx in target_idxs:
                if distances.get(source_idx, math.inf) == distances.get(target_idx, math.inf) + 1:
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
