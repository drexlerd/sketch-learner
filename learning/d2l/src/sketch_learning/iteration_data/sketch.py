import dlplan
from termcolor import colored
from clingo import Symbol, Number
from typing import Dict, List, MutableSet
from dataclasses import dataclass, field
from collections import defaultdict, OrderedDict, deque

from ..instance_data.tuple_graph import TupleGraph
from ..instance_data.state_pair import StatePair
from ..instance_data.state_pair_classifier import StatePairClassifier, StatePairClassification
from ..instance_data.instance_data import InstanceData


class SketchRule:
    def __init__(self, sketch, rule_idx: int, dlplan_rule: dlplan.Rule):
        self.sketch = sketch  # parent ptr
        self.id = rule_idx
        self.dlplan_rule = dlplan_rule


class Sketch:
    def __init__(self, dlplan_policy: dlplan.Policy, width: int):
        self.dlplan_policy = dlplan_policy
        self.width = width

    def get_rules(self):
        """
        Attach an index and sketch parent ptr to dlplan rules.
        """
        return [SketchRule(self, rule_idx, dlplan_rule) for rule_idx, dlplan_rule in enumerate(self.dlplan_policy.get_rules())]

    def _verify_delta_optimality(self, instance_data: InstanceData, state_pair_classifier: StatePairClassifier, root_idx_to_closest_subgoal_s_idxs: Dict[int, MutableSet[int]]):
        """
        Returns True iff sketch only classifies delta optimal state pairs as good.
        """
        for root_idx, closest_subgoal_s_idxs in root_idx_to_closest_subgoal_s_idxs.items():
            for s_idx in closest_subgoal_s_idxs:
                if state_pair_classifier.classify(StatePair(root_idx, s_idx)) == StatePairClassification.NOT_DELTA_OPTIMAL:
                    print(colored(f"Not delta optimal state pair is classified as good.", "red", "on_grey"))
                    print("state pair:", f"{str(instance_data.state_space.get_state_ref(root_idx))} -> {str(instance_data.state_space.get_state_ref(s_idx))}")
                    return False
        return True

    def _verify_bounded_width(self, instance_data: InstanceData, tuple_graphs: List[TupleGraph]):
        """
        Returns three parts:
            (1) the closest subgoal states for every alive state,
            (2) the closest subgoal tuples for every alive state, and
            (3) True if the width of every alive state is bounded.
        """
        evaluation_cache = dlplan.EvaluationCache(len(self.dlplan_policy.get_boolean_features()), len(self.dlplan_policy.get_numerical_features()))
        root_idx_to_closest_subgoal_s_idxs = defaultdict(set)
        root_idx_to_closest_subgoal_t_idxs = defaultdict(set)
        state_space = instance_data.state_space
        for root_idx in range(state_space.get_num_states()):
            if not state_space.is_alive(root_idx):
                continue
            tuple_graph = tuple_graphs[root_idx]
            assert tuple_graph is not None
            bounded = False
            source_state = state_space.get_state_ref(root_idx)
            for t_idxs in tuple_graph.t_idxs_by_distance:
                for t_idx in t_idxs:
                    subgoal = True
                    assert tuple_graph.t_idx_to_s_idxs[t_idx]
                    for s_idx in tuple_graph.t_idx_to_s_idxs[t_idx]:
                        target_state = state_space.get_state_ref(s_idx)
                        if self.dlplan_policy.evaluate_lazy(source_state, target_state) is not None:
                            root_idx_to_closest_subgoal_s_idxs[tuple_graph.root_idx].add(s_idx)
                            if state_space.is_deadend(s_idx):
                                print(colored(f"Sketch leads to an unsolvable state", "red", "on_grey"))
                                print(str(target_state))
                                return [], [], False
                        else:
                            subgoal = False
                    if subgoal:
                        root_idx_to_closest_subgoal_t_idxs[tuple_graph.root_idx].add(t_idx)
                        bounded = True
                if bounded:
                    break
            if not bounded:
                print(colored(f"Sketch fails to bound width of a state", "red", "on_grey"))
                print(str(source_state))
                return [], [], False
        return root_idx_to_closest_subgoal_s_idxs, root_idx_to_closest_subgoal_t_idxs, True

    def _verify_acyclicity(self, instance_data: InstanceData, root_idx_to_closest_subgoal_s_idxs: Dict[int, MutableSet[int]]):
        """
        Returns True iff sketch is acyclic, i.e., no infinite trajectories s1,s2,... are possible.
        """
        for root_idx in range(instance_data.state_space.get_num_states()):
            # The depth-first search is the iterative version where the current path is explicit in the stack.
            # https://en.wikipedia.org/wiki/Depth-first_search
            stack = [(root_idx, iter(root_idx_to_closest_subgoal_s_idxs[root_idx]))]
            s_idxs_on_path = {root_idx,}
            frontier = set()  # the generated states, to ensure that they are only added once to the stack
            while stack:
                source_idx, iterator = stack[-1]
                s_idxs_on_path.add(source_idx)
                try:
                    target_idx = next(iterator)
                    if target_idx in s_idxs_on_path:
                        print(colored("Sketch cycles", "red", "on_grey"))
                        for s_idx in s_idxs_on_path:
                            print(f"{s_idx} {str(instance_data.state_space.get_state_ref(s_idx))}")
                        print(f"{target_idx} {str(instance_data.state_space.get_state_ref(target_idx))}")
                        return False
                    if target_idx not in frontier:
                        frontier.add(target_idx)
                        stack.append((target_idx, iter(root_idx_to_closest_subgoal_s_idxs[target_idx])))
                except StopIteration:
                    s_idxs_on_path.discard(source_idx)
                    stack.pop(-1)
        return True

    def _verify_goal_separating_features(self, instance_data: InstanceData):
        """
        Returns True iff sketch features separate goal from nongoal states.
        """
        state_space = instance_data.state_space
        dlplan_policy_features = self.dlplan_policy.get_boolean_features() + self.dlplan_policy.get_numerical_features()
        s_idx_to_feature_valuations = dict()
        for s_idx in range(state_space.get_num_states()):
            s_idx_to_feature_valuations[s_idx] = tuple([feature.evaluate(state_space.get_state_ref(s_idx)) for feature in dlplan_policy_features])
        for s_idx_1 in range(state_space.get_num_states()):
            for s_idx_2 in range(state_space.get_num_states()):
                if (state_space.is_goal(s_idx_1) and not state_space.is_goal(s_idx_2)):
                    if (s_idx_to_feature_valuations[s_idx_1] == s_idx_to_feature_valuations[s_idx_2]):
                        print(colored("Selected features do not separate goals from non goals.", "red", "on_grey"))
                        print("Goal state:", str(state_space.get_state_ref(s_idx_1)), s_idx_to_feature_valuations[s_idx_1])
                        print("Nongoal state:", str(state_space.get_state_ref(s_idx_2)), s_idx_to_feature_valuations[s_idx_2])
                        return False
        return True

    def solves(self, instance_data: InstanceData, tuple_graphs: List[TupleGraph], state_pair_classifier: StatePairClassifier):
        """
        Returns True iff the sketch solves the instance, i.e.,
            (1) subproblems have bounded width,
            (2) sketch only classifies delta optimal state pairs as good,
            (3) sketch is acyclic, and
            (4) sketch features separate goals from nongoal states. """
        root_idx_to_closest_subgoal_s_idxs, root_idx_to_closest_subgoal_t_idxs, has_bounded_width = self._verify_bounded_width(instance_data, tuple_graphs)
        if not has_bounded_width:
            return False
        if not self._verify_delta_optimality(instance_data, state_pair_classifier, root_idx_to_closest_subgoal_s_idxs):
            return False
        if not self._verify_acyclicity(instance_data, root_idx_to_closest_subgoal_s_idxs):
            return False
        if not self._verify_goal_separating_features(instance_data):
            return False
        return True

    def print(self):
        print(self.dlplan_policy.compute_repr())
        print("Numer of sketch rules:", len(self.dlplan_policy.get_rules()))
        print("Number of selected features:", len(self.dlplan_policy.get_boolean_features()) + len(self.dlplan_policy.get_numerical_features()))
        print("Maximum complexity of selected feature:", max([0] + [boolean_feature.compute_complexity() for boolean_feature in self.dlplan_policy.get_boolean_features()] + [numerical_feature.compute_complexity() for numerical_feature in self.dlplan_policy.get_numerical_features()]))
