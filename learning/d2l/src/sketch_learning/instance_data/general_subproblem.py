from collections import defaultdict
from re import sub
import dlplan
import math
import json

from typing import Dict, List, MutableSet, Tuple
from dataclasses import dataclass, field

from collections import deque

from ..util.command import execute, write_file, read_file, create_experiment_workspace
from .instance_data import InstanceData
from .return_codes import ReturnCode


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
class GeneralSubproblemData:
    id: int
    forward_transitions: Dict[int, MutableSet[Transition]]
    expanded_states: MutableSet[int]
    generated_states: MutableSet[int]

    def print(self):
        print("Generalized subproblem:")
        print("    Forward transitions:", self.forward_transitions)
        print("    Expanded states:", self.expanded_states)
        print("    Generated states:", self.generated_states)


class GeneralSubproblemDataFactory:
    def make_general_subproblems(self, config, instance_datas: List[InstanceData], sketch: dlplan.Policy, rule: dlplan.Rule):
        """
        Step 1: Compute closest subgoal state pairs E_s [(s,s_1),(s,s_2),...] for each state s.
                The induced graph G = (S,E) where E = union_{s in S} E_s
                contains a goal path for every alive state.
        Step 2: What subproblems to solve suboptimally?
        """
        general_subproblem_datas = []
        for instance_data in instance_datas:
            for root_idx in range(instance_data.transition_system.get_num_states()):
                if not instance_data.transition_system.is_alive(root_idx):
                    continue
                closest_subgoal_states = self._compute_closest_subgoal_states(instance_data, root_idx, sketch, rule)
                if not closest_subgoal_states:
                    continue
                expanded_states, generated_states, forward_transitions = self._compute_transitions_to_closest_subgoal_states(instance_data, root_idx, closest_subgoal_states)
                general_subproblem_data = GeneralSubproblemData(len(general_subproblem_datas), forward_transitions, expanded_states, generated_states)
                general_subproblem_datas.append(general_subproblem_data)
        return general_subproblem_datas

    def _compute_closest_subgoal_states(self, instance_data: InstanceData, root_idx: int, sketch: dlplan.Policy, rule: dlplan.Rule):
        evaluation_cache = dlplan.EvaluationCache(len(sketch.get_boolean_features()), len(sketch.get_numerical_features()))
        root_context = dlplan.EvaluationContext(root_idx, instance_data.transition_system.states_by_index[root_idx], evaluation_cache)
        if not rule.evaluate_conditions(root_context):
            return set()
        layers = instance_data.transition_system.compute_states_by_distance(root_idx)
        for layer in layers:
            closest_subgoal_states = set()
            for target_idx in layer:
                target_context = dlplan.EvaluationContext(target_idx, instance_data.transition_system.states_by_index[target_idx], evaluation_cache)
                if rule.evaluate_effects(root_context, target_context):
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
        return expanded_states, generated_states, forward_transitions
