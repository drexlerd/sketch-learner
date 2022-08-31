import re
import dlplan
import math
from clingo import Symbol, Number
from typing import Dict, List, MutableSet
from dataclasses import dataclass, field
from collections import defaultdict, OrderedDict, deque

from ..instance_data.tuple_graph import TupleGraph

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

    def verify_d2(self):
        pass

    def _verify_bounded_width(self, instance_data: InstanceData, tuple_graphs: List[TupleGraph]):
        """
        Check whether the width of all subproblems is bounded.
        """
        evaluation_cache = dlplan.EvaluationCache(len(self.dlplan_policy.get_boolean_features()), len(self.dlplan_policy.get_numerical_features()))
        closest_subgoal_states = defaultdict(set)
        closest_subgoal_tuples = defaultdict(set)
        for root_idx in instance_data.transition_system.s_idx_to_dlplan_state.keys():
            dlplan_state = instance_data.transition_system.s_idx_to_dlplan_state[root_idx]
            tg = tuple_graphs[root_idx]
            if tg is None: continue  # no tuple graph indicates that we don't care about the information of this state.
            bounded = False
            source_context = dlplan.EvaluationContext(root_idx, dlplan_state, evaluation_cache)
            for d in range(1, len(tg.s_idxs_by_distance)):
                for t_idx in tg.t_idxs_by_distance[d]:  # check if t_idxs is a subgoal
                    subgoal = True
                    assert tg.t_idx_to_s_idxs[t_idx]
                    for s_idx in tg.t_idx_to_s_idxs[t_idx]:
                        target_state = instance_data.transition_system.s_idx_to_dlplan_state[s_idx]
                        target_context = dlplan.EvaluationContext(s_idx, target_state, evaluation_cache)
                        if self.dlplan_policy.evaluate_lazy(source_context, target_context) is not None \
                            or instance_data.transition_system.is_goal(s_idx):
                            closest_subgoal_states[tg.root_idx].add(s_idx)
                            if instance_data.transition_system.is_deadend(s_idx):
                                print(f"Sketch leads to unsolvable state: {str(target_state)}")
                                return [], [], False
                        else:
                            subgoal = False
                    if subgoal:
                        closest_subgoal_tuples[tg.root_idx].add(t_idx)
                        bounded = True
                if bounded:
                    break
            if not bounded:
                print(f"Sketch fails to solve state: {str(dlplan_state)}")
                return [], [], False
        return closest_subgoal_states, closest_subgoal_tuples, True

    def _verify_acyclicity(self, instance_data: InstanceData, tuple_graphs: List[TupleGraph], closest_subgoal_states: Dict[int, int]):
        """ Check whether there is a cycle in the compatible state pairs
            We use DFS because we know that every state is reachable from the initial state
            We create a forward graph from compatible state pairs to check for termination
        """
        for root_idx in instance_data.transition_system.s_idx_to_dlplan_state.keys():
            if tuple_graphs[root_idx] is None: continue
            # The depth-first search is the iterative version where the current path is explicit in the stack.
            # https://en.wikipedia.org/wiki/Depth-first_search
            stack = [(root_idx, iter(closest_subgoal_states[root_idx]))]
            s_idxs_on_path = {root_idx,}
            frontier = set()  # the generated states, to ensure that they are only added once to the stack
            while stack:
                source_idx, iterator = stack[-1]
                s_idxs_on_path.add(source_idx)
                try:
                    target_idx = next(iterator)
                    if target_idx in s_idxs_on_path:
                        # print(stack)
                        tuple_graphs[root_idx].print()
                        print("Sketch cycles")
                        for s_idx in s_idxs_on_path:
                            print(f"{s_idx} {str(instance_data.transition_system.s_idx_to_dlplan_state[s_idx])}")
                        print(f"{target_idx} {str(instance_data.transition_system.s_idx_to_dlplan_state[target_idx])}")
                        return False
                    if target_idx not in frontier:
                        frontier.add(target_idx)
                        stack.append((target_idx, iter(closest_subgoal_states[target_idx])))
                except StopIteration:
                    s_idxs_on_path.discard(source_idx)
                    stack.pop(-1)
        return True

    def solves(self, instance_data: InstanceData, tuple_graphs: List[TupleGraph]):
        """ Returns True iff the sketch solves the transition system, i.e.,
            (1) is terminating, and (2) P[s] has correctly bounded s-width. """
        closest_subgoal_states, closest_subgoal_tuples, has_bounded_width = self._verify_bounded_width(instance_data, tuple_graphs)
        if not has_bounded_width: return False
        is_acyclic = self._verify_acyclicity(instance_data, tuple_graphs, closest_subgoal_states)
        if not is_acyclic: return False
        return True
