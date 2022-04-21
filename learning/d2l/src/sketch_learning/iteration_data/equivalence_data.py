import dlplan
import math
from typing import Dict, List, MutableSet, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

from ..instance_data.instance_data import InstanceData
from ..instance_data.tuple_graph import TupleGraph
from ..instance_data.transition_system import TransitionSystem
from ..iteration_data.feature_data import FeatureData


@dataclass
class TupleGraphExt:
    """
    A TupleGraphExt makes use of the equivalence classes.

    A subgoal tuple t contains equivalence classes [(s,s')]
    if s' is resulting state of optimal plan for t.
    """
    root_idx: int
    t_idxs_by_distance: List[List[int]]
    r_idxs_by_distance: List[List[int]]
    t_idx_to_r_idxs: Dict[int, MutableSet[int]]
    r_idx_to_deadend_distance: Dict[int, int]
    width: int

    def print(self):
        print(self.t_idxs_by_distance)
        print(self.r_idxs_by_distance)
        print(self.t_idx_to_r_idxs)
        print(self.r_idx_to_deadend_distance)


@dataclass
class TerminationGraph:
    """
    A TerminationGraph for instance I makes use of the equivalence classes
    and is a graph G = (V, E) where V is set of equivalence classes
    and E is set edges where there is an edge from [(s,s')] to [(t, t')] if s' = t
    and s,s',t,t' come from instance I.
    """
    rule_idx_to_state_pairs: Dict[int, List[Tuple[int, int]]]

    def print(self):
        print(self.rule_idx_to_state_pairs)


@dataclass
class InstanceDataExt:
    tuple_graph_ext_by_state_index: List[TupleGraphExt]
    termination_graph: TerminationGraph


class TupleGraphExtFactory:
    def make_tuple_graph_ext(self, tuple_graph: TupleGraph, transition_system: TransitionSystem, state_pair_to_rule_idx: Dict[Tuple[int, int], int]):
        if tuple_graph is None:
            return None
        root_idx = tuple_graph.root_idx
        r_idxs_by_distance = []
        r_idx_to_deadend_distance = dict()
        d = 0
        for layer in tuple_graph.s_idxs_by_distance:
            r_idxs = []
            for s_idx in layer:
                state_pair = (root_idx, s_idx)
                r_idx = state_pair_to_rule_idx[state_pair]
                r_idxs.append(r_idx)
                if transition_system.is_deadend(s_idx):
                    # the first time we write r_idx = d, d is smallest value.
                    if r_idx not in r_idx_to_deadend_distance:
                        r_idx_to_deadend_distance[r_idx] = d
            r_idxs_by_distance.append(r_idxs)
            d += 1
        t_idx_to_r_idxs = defaultdict(set)
        for t_idxs in tuple_graph.t_idxs_by_distance:
            for t_idx in t_idxs:
                for s_idx in tuple_graph.t_idx_to_s_idxs[t_idx]:
                    state_pair = (root_idx, s_idx)
                    r_idx = state_pair_to_rule_idx[state_pair]
                    t_idx_to_r_idxs[t_idx].add(r_idx)
        return TupleGraphExt(root_idx, tuple_graph.t_idxs_by_distance, r_idxs_by_distance, t_idx_to_r_idxs, r_idx_to_deadend_distance, tuple_graph.width)


class TerminationGraphFactory:
    def make_termination_graph(self, rule_idx_to_state_pairs: Dict[int, Tuple[int, int]]):
        return TerminationGraph(rule_idx_to_state_pairs)


@dataclass
class EquivalenceData:
    """
    Two state pairs are equivalent if they are compatible with a rule
    consisting of the same maximal set of feature conditions and effects over feature pool F.

    Then one can define a termination graph G = (V, E)
    where V is nodes of equivalence classes
    and there is a transition ([(s,s')],[(s',t)]) in E

    Next for subgoals we can assign equivalence classes to subgoal tuples
    and require all of them to be true to bound the width.

    For ``good'' equivalence classes we can check against the feature conditions
    and effects in the equivalence classes only considering the selected features.

    """
    rules: List[dlplan.Rule]
    instance_datas_ext: List[InstanceDataExt]


class EquivalenceDataFactory:
    def make_equivalence_class_data(self, selected_instance_datas: List[InstanceData], feature_data: FeatureData):
        policy_builder = dlplan.PolicyBuilder()
        boolean_features = feature_data.boolean_features
        numerical_features = feature_data.numerical_features
        policy_boolean_features = [policy_builder.add_boolean_feature(b) for b in boolean_features]
        policy_numerical_features = [policy_builder.add_numerical_feature(n) for n in numerical_features]
        rules = []
        rule_repr_to_idx = dict()
        count_state_pairs = 0
        selected_instance_datas_ext = []
        for i in range(len(selected_instance_datas)):
            rule_idx_to_state_pairs = defaultdict(list)
            state_pair_to_rule_idx = dict()
            instance = selected_instance_datas[i]
            numerical_feature_valuations = feature_data.numerical_feature_valuations[i]
            boolean_feature_valuations = feature_data.boolean_feature_valuations[i]
            tuple_graph_ext_by_state_index = []
            for tg in instance.tuple_graphs_by_state_index:
                if tg is None:
                    tuple_graph_ext_by_state_index.append(None)
                    continue
                root_idx = tg.root_idx
                # add conditions
                conditions = []
                for n_idx in range(len(numerical_features)):
                    if numerical_feature_valuations[root_idx][n_idx] > 0:
                        conditions.append(policy_builder.add_gt_condition(policy_numerical_features[n_idx]))
                    else:
                        conditions.append(policy_builder.add_eq_condition(policy_numerical_features[n_idx]))
                for b_idx in range(len(boolean_features)):
                    if boolean_feature_valuations[root_idx][b_idx]:
                        conditions.append(policy_builder.add_pos_condition(policy_boolean_features[b_idx]))
                    else:
                        conditions.append(policy_builder.add_neg_condition(policy_boolean_features[b_idx]))
                # add effects
                for s_idxs in tg.s_idxs_by_distance:
                    count_state_pairs += len(s_idxs)
                    for s_idx in s_idxs:
                        effects = []
                        for n_idx in range(len(numerical_features)):
                            if numerical_feature_valuations[root_idx][n_idx] > numerical_feature_valuations[s_idx][n_idx]:
                                effects.append(policy_builder.add_dec_effect(policy_numerical_features[n_idx]))
                            elif numerical_feature_valuations[root_idx][n_idx] < numerical_feature_valuations[s_idx][n_idx]:
                                effects.append(policy_builder.add_inc_effect(policy_numerical_features[n_idx]))
                            else:
                                effects.append(policy_builder.add_bot_effect(policy_numerical_features[n_idx]))
                        for b_idx in range(len(boolean_features)):
                            if boolean_feature_valuations[root_idx][b_idx] and not boolean_feature_valuations[s_idx][b_idx]:
                                effects.append(policy_builder.add_neg_effect(policy_boolean_features[b_idx]))
                            elif not boolean_feature_valuations[root_idx][b_idx] and boolean_feature_valuations[s_idx][b_idx]:
                                effects.append(policy_builder.add_pos_effect(policy_boolean_features[b_idx]))
                            else:
                                effects.append(policy_builder.add_bot_effect(policy_boolean_features[b_idx]))
                        # add rule
                        rule = policy_builder.add_rule(conditions, effects)
                        rule_repr = rule.compute_repr()
                        if rule_repr in rule_repr_to_idx:
                            rule_idx = rule_repr_to_idx[rule_repr]
                        else:
                            rule_idx = len(rules)
                            rule_repr_to_idx[rule_repr] = rule_idx
                            rules.append(rule)
                        state_pair = (root_idx, s_idx)
                        rule_idx_to_state_pairs[rule_idx].append(state_pair)
                        state_pair_to_rule_idx[state_pair] = rule_idx
                tuple_graph_ext = TupleGraphExtFactory().make_tuple_graph_ext(tg, instance.transition_system, state_pair_to_rule_idx)
                tuple_graph_ext_by_state_index.append(tuple_graph_ext)
            termination_graph = TerminationGraphFactory().make_termination_graph(rule_idx_to_state_pairs)
            selected_instance_datas_ext.append(InstanceDataExt(tuple_graph_ext_by_state_index, termination_graph))
        assert count_state_pairs >= len(rules)
        print(f"Num state pairs: {count_state_pairs}")
        print(f"Num rules: {len(rules)}")

        return EquivalenceData(rules, selected_instance_datas_ext)