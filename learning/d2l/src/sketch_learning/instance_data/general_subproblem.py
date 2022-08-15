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
class GeneralSubproblemData:
    forward_transitions: Dict[int, List[MutableSet[Transition]]]  # there can be disjunctive sets of optimal transitions for a state
    expanded_states: MutableSet[int]
    generated_states: MutableSet[int]

    def is_consistent(self):
        return all([(len(transitions) == 1) for transitions in self.forward_transitions.values()])

    def print(self):
        print("Generalized subproblem:")
        print("    Forward transitions:", self.forward_transitions)
        print("    Expanded states:", self.expanded_states)
        print("    Generated states:", self.generated_states)
        print("    Consistent: ", self.is_consistent())


class GeneralSubproblemDataFactory:
    def make_general_subproblems(self, instance_datas: List[InstanceData], sketch: dlplan.Policy, rule: dlplan.Rule):
        """
        Step 1: Compute closest subgoal state pairs E_s [(s,s_1),(s,s_2),...] for each state s.
                The induced graph G = (S,E) where E = union_{s in S} E_s
                contains a goal path for every alive state.
        Step 2: What subproblems to solve suboptimally?
        """
        general_subproblem_datas = []
        for instance_data in instance_datas:
            general_subproblem_data = self.make_general_subproblem(instance_data, sketch, rule)
            general_subproblem_datas.append(general_subproblem_data)
        return general_subproblem_datas

    def make_general_subproblem(self, instance_data: InstanceData, sketch: dlplan.Policy, rule: dlplan.Rule):
        expanded_states = set()
        generated_states = set()
        forward_transitions = defaultdict(set)
        for root_idx in range(instance_data.transition_system.get_num_states()):
            if not instance_data.transition_system.is_alive(root_idx): continue
            closest_subgoal_states = self._compute_closest_subgoal_states(instance_data, root_idx, sketch, rule)
            if not closest_subgoal_states: continue
            relevant_expanded_states, relevant_generated_states, relevant_forward_transitions = self._compute_transitions_to_closest_subgoal_states(instance_data, root_idx, closest_subgoal_states)
            expanded_states.update(relevant_expanded_states)
            generated_states.update(relevant_generated_states)
            for source_idx, transitions in relevant_forward_transitions.items():
                forward_transitions[source_idx].add(frozenset(transitions))
        # filter minimal transitions
        result_forward_transitions = defaultdict(set)
        for root_idx, transitionss in forward_transitions.items():
            prec = defaultdict(set)
            for transitions_1 in transitionss:
                for transitions_2 in transitionss:
                    if transitions_1 == transitions_2: continue
                    if transitions_1.issubset(transitions_2):
                        prec[transitions_2].add(transitions_1)
            selected_transitions = set()
            for transitions in transitionss:
                if len(prec[transitions]) == 0 and transitions not in selected_transitions:
                    result_forward_transitions[root_idx].add(transitions)
                    selected_transitions.add(transitions)
        return GeneralSubproblemData(forward_transitions, expanded_states, generated_states)

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
        return expanded_states, generated_states, relevant_forward_transitions
