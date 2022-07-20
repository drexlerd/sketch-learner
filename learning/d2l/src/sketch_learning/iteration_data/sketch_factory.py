import re
import dlplan
import math
from typing import Dict, List, MutableSet
from dataclasses import dataclass, field
from collections import defaultdict, OrderedDict, deque

from ..asp.answer_set_parser import AnswerSetData
from .feature_data import DomainFeatureData
from ..instance_data.instance_data import InstanceData


class Sketch:
    def __init__(self, policy: dlplan.Policy, width: int):
        self.policy = policy
        self.width = width

    def _verify_bounded_width(self, instance_data: InstanceData):
        """ Check whether the width of all subproblems is bounded.
        """
        self.policy.clear_cache()
        closest_subgoal_states = defaultdict(set)
        closest_subgoal_tuples = defaultdict(set)
        for root_idx in range(instance_data.transition_system.get_num_states()):
            dlplan_state = instance_data.transition_system.states_by_index[root_idx]
            tg = instance_data.tuple_graphs_by_state_index[root_idx]
            if tg is None: continue  # no tuple graph indicates that we don't care about the information of this state.
            bounded = False
            if tg.width == 0:
                low = 1
            else:
                low = 0
            for d in range(low, len(tg.s_idxs_by_distance)):
                for t_idx in tg.t_idxs_by_distance[d]:  # check if t_idxs is a subgoal
                    subgoal = True
                    assert tg.t_idx_to_s_idxs[t_idx]
                    for s_idx in tg.t_idx_to_s_idxs[t_idx]:
                        target_state = instance_data.transition_system.states_by_index[s_idx]
                        if self.policy.evaluate_lazy(root_idx, dlplan_state, s_idx, target_state) is None:
                            subgoal = False
                        else:
                            closest_subgoal_states[tg.root_idx].add(s_idx)
                            if instance_data.transition_system.is_deadend(s_idx):
                                print(f"Sketch leads to unsolvable state: {str(target_state)}")
                                return [], [], False
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
        for state in instance_data.transition_system.states_by_index:
            print(str(state))
        for root_idx in range(instance_data.transition_system.get_num_states()):
            if instance_data.tuple_graphs_by_state_index[root_idx] is None: continue
            optimal_forward_transitions, _ = instance_data.transition_system.compute_optimal_transitions_to_states(closest_subgoal_states[root_idx])
            # filter only transitions on optimal paths to subgoal
            relevant_optimal_forward_transitions = defaultdict(set)
            alive_s_idxs_on_optimal_paths = set()
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
            print(alive_s_idxs_on_optimal_paths)
            for alive_s_idx in alive_s_idxs_on_optimal_paths:
                if not (closest_subgoal_tuples[root_idx].issubset(closest_subgoal_tuples[alive_s_idx]) or \
                        closest_subgoal_tuples[root_idx] == closest_subgoal_tuples[alive_s_idx]):
                    print(closest_subgoal_tuples[root_idx])
                    print(closest_subgoal_tuples[alive_s_idx])
                    # if cst[r] > cst[a] then we must ensure the opposite, i.e., cst[r] <= cst[a]
                    # Hence, for all t in cst[r]: if subgoal(r, t) then subgoal(a, t)
                    for t_idx in closest_subgoal_tuples[root_idx]:
                        consistency_facts.append(f"consisteny({instance_idx},{root_idx},{alive_s_idx},{t_idx}).")
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


class SketchFactory:
    def make_sketch(self, answer_set_data: AnswerSetData, domain_feature_data: DomainFeatureData, width: int):
        """ Parses set of facts into dlplan.Policy """
        policy_builder = dlplan.PolicyBuilder()
        boolean_policy_features, numerical_policy_features = self._add_features(policy_builder, answer_set_data, domain_feature_data)
        self._add_rules(policy_builder, answer_set_data, boolean_policy_features, numerical_policy_features)
        return Sketch(policy_builder.get_result(), width)


    def _add_features(self, policy_builder: dlplan.PolicyBuilder, answer_set_data: AnswerSetData, domain_feature_data: DomainFeatureData):
        f_idx_to_boolean_policy_feature = dict()
        f_idx_to_numerical_policy_feature = dict()
        for fact in answer_set_data.facts:
            matches = re.findall(r"select\(([bn])(\d+)\)", fact)
            if matches:
                assert len(matches) == 1
                f_type = matches[0][0]
                f_idx = int(matches[0][1])
                if f_type == "b":
                    f_idx_to_boolean_policy_feature[f_idx] = policy_builder.add_boolean_feature(domain_feature_data.boolean_features[f_idx])
                elif f_type == "n":
                    f_idx_to_numerical_policy_feature[f_idx] = policy_builder.add_numerical_feature(domain_feature_data.numerical_features[f_idx])
                else:
                    raise Exception("Cannot parse feature {fact}")
        return f_idx_to_boolean_policy_feature, f_idx_to_numerical_policy_feature

    def _add_rules(self, policy_builder: dlplan.PolicyBuilder, answer_set_data: AnswerSetData, boolean_policy_features, numerical_policy_features):
        rules = dict()
        for fact in answer_set_data.facts:
            matches = re.findall(r"rule\((\d+)\)", fact)
            if matches:
                assert len(matches) == 1
                r_key = int(matches[0])
                rules[r_key] = [[], []]  # conditions and effects
        for fact in answer_set_data.facts:
            self._try_parse_condition(r"c_eq\((\d+),n(\d+)\)", fact, rules, policy_builder.add_eq_condition, numerical_policy_features)
            self._try_parse_condition(r"c_gt\((\d+),n(\d+)\)", fact, rules, policy_builder.add_gt_condition, numerical_policy_features)
            self._try_parse_condition(r"c_pos\((\d+),b(\d+)\)", fact, rules, policy_builder.add_pos_condition, boolean_policy_features)
            self._try_parse_condition(r"c_neg\((\d+),b(\d+)\)", fact, rules, policy_builder.add_neg_condition, boolean_policy_features)
            self._try_parse_effect(r"e_inc\((\d+),n(\d+)\)", fact, rules, policy_builder.add_inc_effect, numerical_policy_features)
            self._try_parse_effect(r"e_dec\((\d+),n(\d+)\)", fact, rules, policy_builder.add_dec_effect, numerical_policy_features)
            self._try_parse_effect(r"e_bot\((\d+),n(\d+)\)", fact, rules, policy_builder.add_bot_effect, numerical_policy_features)
            self._try_parse_effect(r"e_pos\((\d+),b(\d+)\)", fact, rules, policy_builder.add_pos_effect, boolean_policy_features)
            self._try_parse_effect(r"e_neg\((\d+),b(\d+)\)", fact, rules, policy_builder.add_neg_effect, boolean_policy_features)
            self._try_parse_effect(r"e_bot\((\d+),b(\d+)\)", fact, rules, policy_builder.add_bot_effect, boolean_policy_features)
        for _, (conditions, effects) in rules.items():
            policy_builder.add_rule(conditions, effects)

    def _try_parse_condition(self, regex, fact, rules, policy_builder_func, f_idx_to_policy_feature):
        matches = re.findall(regex, fact)
        if matches:
            assert len(matches) == 1
            r_key = int(matches[0][0])
            f_idx = int(matches[0][1])
            if f_idx in f_idx_to_policy_feature:
                rules[r_key][0].append(policy_builder_func(f_idx_to_policy_feature[f_idx]))

    def _try_parse_effect(self, regex, fact, rules, policy_builder_func, f_idx_to_policy_feature):
        matches = re.findall(regex, fact)
        if matches:
            assert len(matches) == 1
            r_key = int(matches[0][0])
            f_idx = int(matches[0][1])
            if f_idx in f_idx_to_policy_feature:
                rules[r_key][1].append(policy_builder_func(f_idx_to_policy_feature[f_idx]))
