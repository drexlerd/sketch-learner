import re
import dlplan
import math
from clingo import Model
from typing import Dict, List, MutableSet
from dataclasses import dataclass, field
from collections import defaultdict, OrderedDict, deque

from ..instance_data.instance_data import InstanceData


class Sketch:
    def __init__(self, policy: dlplan.Policy, width: int):
        self.policy = policy
        self.width = width

    def _verify_bounded_width(self, instance_data: InstanceData):
        """ Check whether the width of all subproblems is bounded.
        """
        evaluation_cache = dlplan.EvaluationCache(len(self.policy.get_boolean_features()), len(self.policy.get_numerical_features()))
        closest_subgoal_states = defaultdict(set)
        closest_subgoal_tuples = defaultdict(set)
        for root_idx in range(instance_data.transition_system.get_num_states()):
            dlplan_state = instance_data.transition_system.states_by_index[root_idx]
            tg = instance_data.tuple_graphs_by_state_index[root_idx]
            if tg is None: continue  # no tuple graph indicates that we don't care about the information of this state.
            bounded = False
            source_context = dlplan.EvaluationContext(root_idx, dlplan_state, evaluation_cache)
            if tg.width == 0:
                low = 1
            else:
                low = 0
            for d in range(low, len(tg.s_idxs_by_distance)):
                for t_idx in tg.t_idxs_by_distance[d]:  # check if t_idxs is a subgoal
                    if root_idx == 1 and d == 3: print(t_idx)
                    subgoal = True
                    assert tg.t_idx_to_s_idxs[t_idx]
                    for s_idx in tg.t_idx_to_s_idxs[t_idx]:
                        target_state = instance_data.transition_system.states_by_index[s_idx]
                        target_context = dlplan.EvaluationContext(s_idx, target_state, evaluation_cache)
                        if self.policy.evaluate_lazy(source_context, target_context) is not None \
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

    def _verify_acyclicity(self, instance_data: InstanceData, closest_subgoal_states: Dict[int, int]):
        """ Check whether there is a cycle in the compatible state pairs
            We use DFS because we know that every state is reachable from the initial state
            We create a forward graph from compatible state pairs to check for termination
        """
        for root_idx in range(instance_data.transition_system.get_num_states()):
            if instance_data.tuple_graphs_by_state_index[root_idx] is None: continue
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
                        print("Sketch cycles")
                        for s_idx in s_idxs_on_path:
                            print(f"{s_idx} {str(instance_data.transition_system.states_by_index[s_idx])}")
                        print(f"{target_idx} {str(instance_data.transition_system.states_by_index[target_idx])}")
                        return False
                    if target_idx not in frontier:
                        frontier.add(target_idx)
                        stack.append((target_idx, iter(closest_subgoal_states[target_idx])))
                except StopIteration:
                    s_idxs_on_path.discard(source_idx)
                    stack.pop(-1)
        return True

    def verify_consistency(self, instance_idx: int, instance_data: InstanceData):
        """
        """
        is_consistent = True
        consistency_facts = []
        # 1. compute subgoal tuples for each state
        closest_subgoal_states, closest_subgoal_tuples, has_bounded_width = self._verify_bounded_width(instance_data)
        # 2. For each state s with subgoal tuples T check whether every state s'
        #    that is on an optimal path from s to T with subgoal tuples T'
        #    holds that T' subseteq T
        for s_idx, state in enumerate(instance_data.transition_system.states_by_index):
            print(s_idx, str(state))
        for root_idx in range(instance_data.transition_system.get_num_states()):
            if instance_data.tuple_graphs_by_state_index[root_idx] is None: continue
            optimal_forward_transitions, _ = instance_data.transition_system.compute_optimal_transitions_to_states(closest_subgoal_states[root_idx])
            # filter only transitions on optimal paths to subgoal
            relevant_optimal_forward_transitions = defaultdict(set)
            alive_s_idxs_on_optimal_paths = {root_idx}
            distances = dict()
            queue = deque()
            distances[root_idx] = 0
            queue.append(root_idx)
            while queue:
                source_idx = queue.popleft()
                source_cost = distances.get(source_idx)
                for target_idx in optimal_forward_transitions[source_idx]:
                    alt_distance = source_cost + 1
                    if alt_distance < distances.get(target_idx, math.inf):
                        distances[target_idx] = alt_distance
                        queue.append(target_idx)
                    if alt_distance == distances.get(target_idx):
                        if target_idx not in closest_subgoal_states[source_idx]:
                            alive_s_idxs_on_optimal_paths.add(target_idx)
                        relevant_optimal_forward_transitions[source_idx].add(target_idx)
            print(root_idx, closest_subgoal_states, alive_s_idxs_on_optimal_paths, relevant_optimal_forward_transitions)
            for alive_s_idx in alive_s_idxs_on_optimal_paths:
                if not (closest_subgoal_tuples[root_idx].issubset(closest_subgoal_tuples[alive_s_idx]) or \
                        closest_subgoal_tuples[root_idx] == closest_subgoal_tuples[alive_s_idx]):
                    print(closest_subgoal_tuples[root_idx])
                    print(closest_subgoal_tuples[alive_s_idx])
                    # if cst[r] > cst[a] then we must ensure the opposite, i.e., cst[r] <= cst[a]
                    # Hence, for all t in cst[r]: if subgoal(r, t) then subgoal(a, t)
                    for t_idx in closest_subgoal_tuples[root_idx]:
                        consistency_facts.append(("consisteny", [instance_idx, root_idx, alive_s_idx, t_idx]))
                    print("inconsistent")
                    exit(1)
                #print(closest_subgoal_tuples[alive_s_idx])
                #print(closest_subgoal_states[alive_s_idx])
            #print(root_idx)
            #print(closest_subgoal_states[root_idx])
            #print(optimal_forward_transitions)
            #print(relevant_optimal_forward_transitions)
            #print(alive_s_idxs_on_optimal_paths)
            #print()
        return is_consistent, consistency_facts

    def solves(self, instance_data: InstanceData):
        """ Returns True iff the sketch solves the transition system, i.e.,
            (1) is terminating, and (2) P[s] has correctly bounded s-width. """
        closest_subgoal_states, closest_subgoal_tuples, has_bounded_width = self._verify_bounded_width(instance_data)
        if not has_bounded_width: return False
        is_acyclic = self._verify_acyclicity(instance_data, closest_subgoal_states)
        if not is_acyclic: return False
        return True
