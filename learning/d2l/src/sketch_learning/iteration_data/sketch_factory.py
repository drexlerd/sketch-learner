import re
import dlplan
import copy
from typing import Dict, List, MutableSet
from dataclasses import dataclass, field
from collections import defaultdict
from ..asp.answer_set_parser import AnswerSetData
from .feature_data import FeatureData
from ..instance_data.instance_data import InstanceData


class Sketch:
    def __init__(self, policy: dlplan.Policy, width: int):
        self.policy = policy
        self.width = width

    def solves(self, instance_data: InstanceData):
        """ Returns True iff the sketch solves the transition system, i.e.,
            (1) is terminating, and (2) P[s] has correctly bounded width. """
        # 1. Check if the width of all subproblems is bounded
        # we clear the in to be able to reuse cache with instance specific indexing scheme.
        self.policy.clear_cache()
        closest_subgoal_tuple = dict()
        for i in range(instance_data.transition_system.get_num_states()):
            dlplan_state = instance_data.transition_system.states_by_index[i]
            tg = instance_data.tuple_graphs_by_state_index[i]
            if tg is None:
                continue  # no tuple graph indicates that we don't care about the information of this state.
            bounded = False
            for d in range(1, len(tg.s_idxs_by_distance)):
                for t_idx in tg.t_idxs_by_distance[d]:  # check if t_idxs is a subgoal
                    subgoal = True
                    assert tg.t_idx_to_s_idxs[t_idx]
                    for s_idx in tg.t_idx_to_s_idxs[t_idx]:
                        target_state = instance_data.transition_system.states_by_index[s_idx]
                        if self.policy.evaluate_lazy(i, dlplan_state, s_idx, target_state) is None:
                            subgoal = False
                            break
                    if subgoal:
                        bounded = True
                        break
                if bounded:
                    closest_subgoal_tuple[i] = d
                    break
            if not bounded:
                print(f"Sketch fails to solve state: {str(dlplan_state)}")
                return False
        # 2. Check whether there is a cycle in the compatible state pairs
        # We use DFS because we know that every state is reachable from the initial state
        # We create a forward graph from compatible state pairs to check for termination
        subgoals = defaultdict(set)
        for i in range(instance_data.transition_system.get_num_states()):
            dlplan_state = instance_data.transition_system.states_by_index[i]
            tg = instance_data.tuple_graphs_by_state_index[i]
            if tg is None:
                continue  # no tuple graph indicates that we don't care about the information of this state.
            for d in range(1, closest_subgoal_tuple[i] + 1):
                for s_idx in tg.s_idxs_by_distance[d]:
                    target_state = instance_data.transition_system.states_by_index[s_idx]
                    if self.policy.evaluate_lazy(i, dlplan_state, s_idx, target_state) is not None:
                        if instance_data.transition_system.is_deadend(s_idx) and d <= closest_subgoal_tuple[i]:
                            print(f"Sketch leads to unsolvable state: {str(target_state)}")
                            return False
                        subgoals[i].add(s_idx)
                        break
        expanded_global = set(subgoals.keys())
        while expanded_global:
            # The depth-first search is the iterative version where the current path is explicit in the stack.
            # https://en.wikipedia.org/wiki/Depth-first_search
            root_idx = expanded_global.pop()
            stack = [(root_idx, iter(subgoals[root_idx]))]
            s_idxs_on_path = {root_idx,}
            frontier = set()  # the generated states, to ensure that they are only added once to the stack
            while stack:
                source_idx, iterator = stack[-1]
                s_idxs_on_path.add(source_idx)
                try:
                    target_idx = next(iterator)
                    if target_idx in s_idxs_on_path:
                        print("Sketch cycles")
                        for s_idx in s_idxs_on_path:
                            print(str(instance_data.transition_system.states_by_index[s_idx]))
                        print(str(instance_data.transition_system.states_by_index[target_idx]))
                        return False
                    if target_idx not in frontier:
                        frontier.add(target_idx)
                        stack.append((target_idx, iter(subgoals[target_idx])))
                except StopIteration:
                    s_idxs_on_path.discard(source_idx)
                    stack.pop(-1)
                    expanded_global.discard(source_idx)
        return True


class SketchFactory:
    def make_sketch(self, answer_set_data: AnswerSetData, feature_data: FeatureData, width: int):
        """ Parses set of facts into dlplan.Policy """
        policy_builder = dlplan.PolicyBuilder()
        f_idx_to_policy_feature = self._add_features(policy_builder, answer_set_data, feature_data)
        self._add_rules(policy_builder, answer_set_data, f_idx_to_policy_feature)
        return Sketch(policy_builder.get_result(), width)


    def _add_features(self, policy_builder: dlplan.PolicyBuilder, answer_set_data: AnswerSetData, feature_data: FeatureData):
        f_idx_to_policy_feature = dict()
        for fact in answer_set_data.facts:
            matches = re.findall(r"select\((\d+)\)", fact)
            if matches:
                assert len(matches) == 1
                f_idx = int(matches[0])
                if f_idx < len(feature_data.boolean_features):
                    policy_feature = policy_builder.add_boolean_feature(feature_data.boolean_features[f_idx])
                else:
                    policy_feature = policy_builder.add_numerical_feature(feature_data.numerical_features[f_idx - len(feature_data.boolean_features)])
                f_idx_to_policy_feature[f_idx] = policy_feature
        return f_idx_to_policy_feature

    def _add_rules(self, policy_builder: dlplan.PolicyBuilder, answer_set_data: AnswerSetData, f_idx_to_policy_feature):
        rules = dict()
        for fact in answer_set_data.facts:
            matches = re.findall(r"rule\((\d+)\)", fact)
            if matches:
                assert len(matches) == 1
                r_key = int(matches[0])
                rules[r_key] = [[], []]  # conditions and effects
        for fact in answer_set_data.facts:
            self._try_parse_condition(r"c_eq\((\d+),(\d+)\)", fact, rules, policy_builder.add_eq_condition, f_idx_to_policy_feature)
            self._try_parse_condition(r"c_gt\((\d+),(\d+)\)", fact, rules, policy_builder.add_gt_condition, f_idx_to_policy_feature)
            self._try_parse_condition(r"c_pos\((\d+),(\d+)\)", fact, rules, policy_builder.add_pos_condition, f_idx_to_policy_feature)
            self._try_parse_condition(r"c_neg\((\d+),(\d+)\)", fact, rules, policy_builder.add_neg_condition, f_idx_to_policy_feature)
            self._try_parse_effect(r"e_inc\((\d+),(\d+)\)", fact, rules, policy_builder.add_inc_effect, f_idx_to_policy_feature)
            self._try_parse_effect(r"e_dec\((\d+),(\d+)\)", fact, rules, policy_builder.add_dec_effect, f_idx_to_policy_feature)
            self._try_parse_effect(r"e_pos\((\d+),(\d+)\)", fact, rules, policy_builder.add_pos_effect, f_idx_to_policy_feature)
            self._try_parse_effect(r"e_neg\((\d+),(\d+)\)", fact, rules, policy_builder.add_neg_effect, f_idx_to_policy_feature)
            self._try_parse_effect(r"e_bot\((\d+),(\d+)\)", fact, rules, policy_builder.add_bot_effect, f_idx_to_policy_feature)
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
