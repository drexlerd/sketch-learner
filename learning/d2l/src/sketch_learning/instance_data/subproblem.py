from collections import defaultdict
from re import sub
import dlplan
import math
import json

from typing import Dict, List, MutableSet, Tuple
from dataclasses import dataclass, field

from collections import deque

from ..util.command import execute, write_file, read_file, create_experiment_workspace
from ..iteration_data.sketch import SketchRule

from .instance_data import InstanceData, InstanceDataFactory
from .return_codes import ReturnCode


class SubproblemJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Transition):
            return [obj.source_idx, obj.target_idx, obj.optimal]
        elif isinstance(obj, set):
            return list(obj)
        else:
            return json.JSONEncoder.default(self, obj)


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
class SubproblemData:
    id: int
    instance_data: InstanceData
    root_idx: int
    forward_transitions: Dict[int, MutableSet[Transition]]
    expanded_states: MutableSet[int]
    generated_states: MutableSet[int]

    def print(self):
        print("Subproblem:")
        print("    Root index:", self.root_idx)
        print("    Forward transitions:", self.forward_transitions)
        print("    Expanded states:", self.expanded_states)
        print("    Generated states:", self.generated_states)

    def dump_json(self, filename):
        with open(filename, "w") as file:
            data = {
                "root_idx": self.root_idx,
                "forward_transitions": self.forward_transitions,
                "expanded_states": self.expanded_states,
                "generated_states": self.generated_states
            }
            json.dump(data, file, indent=4, cls=SubproblemJsonEncoder)


class SubproblemDataFactory:
    def make_subproblems(self, config, instance_datas: List[InstanceData], rule: SketchRule):
        subproblem_datas = []
        for instance_data in instance_datas:
            #rule_dir = config.instance_informations[instance_data.id].workspace / f"rule_{rule.id}"
            #create_experiment_workspace(rule_dir, True)
            for root_idx in range(instance_data.transition_system.get_num_states()):
                if not instance_data.transition_system.is_alive(root_idx):
                    continue
                closest_subgoal_states = self._compute_closest_subgoal_states(instance_data, root_idx, rule)
                if not closest_subgoal_states:
                    continue
                expanded_states, generated_states, forward_transitions = self._compute_transitions_to_closest_subgoal_states(instance_data, root_idx, closest_subgoal_states)
                # filename = rule_dir / f"subproblem_{subproblem_data.id}.json"
                subproblem_data = SubproblemData(len(subproblem_datas), instance_data, root_idx, forward_transitions, expanded_states, generated_states)
                # general_subproblem_data.dump_json(filename)
                subproblem_datas.append(subproblem_data)
        # sort by number of generated states and fix the broken indexing scheme
        sorted(subproblem_datas, key=lambda x : len(x.generated_states))
        for subproblem_idx, subproblem_data in enumerate(subproblem_datas):
            subproblem_data.id = subproblem_idx
        return subproblem_datas

    def make_subproblem_instance_datas(self, config, subproblem_datas: List[SubproblemData]):
        subproblem_instance_datas = []
        for subproblem_data in subproblem_datas:
            subproblem_instance_data = InstanceDataFactory().reparse_instance_data(subproblem_data.instance_data)
            # add static seed atoms for initial state
            for atom_idx in subproblem_instance_data.transition_system.states_by_index[subproblem_data.root_idx].get_atom_idxs():
                atom = subproblem_instance_data.instance_info.get_atom(atom_idx)
                subproblem_instance_data.instance_info.add_static_atom(atom.get_predicate().get_name() + "_r", [object.get_name() for object in atom.get_objects()])
            print([str(atom) for atom in subproblem_instance_data.instance_info.get_static_atoms()])
            exit(1)
            subproblem_instance_datas.append(subproblem_instance_data)
        return subproblem_instance_datas

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
