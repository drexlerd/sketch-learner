import dlplan
import math
from typing import Dict, List, MutableSet, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

from ..instance_data.instance_data import InstanceData
from ..instance_data.tuple_graph import TupleGraph
from ..instance_data.transition_system import TransitionSystem
from ..iteration_data.feature_data import DomainFeatureData, InstanceFeatureData


@dataclass
class TupleGraphExt:
    """
    A TupleGraphExt makes use of the equivalence classes.

    A subgoal tuple t contains equivalence classes [(s,s')]
    if s' is resulting state of optimal plan for t.
    """
    root_idx: int
    width: int
    t_idxs_by_distance: List[List[int]]
    r_idxs_by_distance: List[List[int]]
    t_idx_to_r_idxs: Dict[int, MutableSet[int]]
    r_idx_to_t_idxs: Dict[int, MutableSet[int]]
    r_idx_to_s_idxs: Dict[int, MutableSet[int]]
    r_idx_to_deadend_distance: Dict[int, int]

    def print(self):
        print("Tuple graph extension state {self.root_idx} and width {self.width}")
        print(self.t_idxs_by_distance)
        print(self.r_idxs_by_distance)
        print(self.r_idx_to_t_idxs)
        print(self.r_idx_to_s_idxs)
        print(self.t_idx_to_r_idxs)
        print(self.r_idx_to_deadend_distance)


@dataclass
class InstanceDataExt:
    tuple_graph_ext_by_state_index: List[TupleGraphExt]


class TupleGraphExtFactory:
    def make_tuple_graph_ext(self, tuple_graph: TupleGraph, transition_system: TransitionSystem, s_idx_to_r_idx: Dict[int, int], r_idx_to_s_idxs):
        if tuple_graph is None:
            return None
        root_idx = tuple_graph.root_idx
        r_idxs_by_distance = []
        r_idx_to_deadend_distance = dict()
        for d, layer in enumerate(tuple_graph.s_idxs_by_distance):
            r_idxs = []
            for s_idx in layer:
                r_idx = s_idx_to_r_idx[s_idx]
                r_idxs.append(r_idx)
                if transition_system.is_deadend(s_idx):
                    # the first time we write r_idx = d, d is smallest value.
                    r_idx_to_deadend_distance[r_idx] = min(r_idx_to_deadend_distance.get(r_idx, math.inf), d)
            r_idxs_by_distance.append(r_idxs)
        t_idx_to_r_idxs = defaultdict(set)
        r_idx_to_t_idxs = defaultdict(set)
        for t_idxs in tuple_graph.t_idxs_by_distance:
            for t_idx in t_idxs:
                for s_idx in tuple_graph.t_idx_to_s_idxs[t_idx]:
                    r_idx = s_idx_to_r_idx[s_idx]
                    t_idx_to_r_idxs[t_idx].add(r_idx)
                    r_idx_to_t_idxs[r_idx].add(t_idx)
        return TupleGraphExt(root_idx, tuple_graph.width, tuple_graph.t_idxs_by_distance, r_idxs_by_distance, t_idx_to_r_idxs, r_idx_to_t_idxs, r_idx_to_s_idxs, r_idx_to_deadend_distance)


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
    instance_data_exts: List[InstanceDataExt]


class EquivalenceDataFactory:
    def make_equivalence_class_data(self, instance_datas: List[InstanceData], domain_feature_data: DomainFeatureData, instance_feature_datas: List[InstanceFeatureData]):
        policy_builder = dlplan.PolicyBuilder()
        policy_boolean_features = [policy_builder.add_boolean_feature(b) for b in domain_feature_data.boolean_features]
        policy_numerical_features = [policy_builder.add_numerical_feature(n) for n in domain_feature_data.numerical_features]
        rules = []
        rule_repr_to_idx = dict()
        count_state_pairs = 0
        instance_datas_ext = []
        for instance_data, instance_feature_data in zip(instance_datas, instance_feature_datas):
            tuple_graph_ext_by_state_index = []
            for tg in instance_data.tuple_graphs_by_state_index:
                if tg is None:
                    tuple_graph_ext_by_state_index.append(None)
                    continue
                r_idx_to_s_idxs = defaultdict(list)
                s_idx_to_r_idx = dict()
                # add conditions
                conditions = self._make_conditions(policy_builder, tg.root_idx, policy_boolean_features, policy_numerical_features, instance_feature_data)
                # add effects
                for s_idxs in tg.s_idxs_by_distance:
                    count_state_pairs += len(s_idxs)
                    for target_idx in s_idxs:
                        effects = self._make_effects(policy_builder, tg.root_idx, target_idx, policy_boolean_features, policy_numerical_features, instance_feature_data)
                        # add rule
                        rule = policy_builder.add_rule(conditions, effects)
                        rule_repr = rule.compute_repr()
                        if rule_repr in rule_repr_to_idx:
                            r_idx = rule_repr_to_idx[rule_repr]
                        else:
                            r_idx = len(rules)
                            rule_repr_to_idx[rule_repr] = r_idx
                            rules.append(rule)
                        r_idx_to_s_idxs[r_idx].append(target_idx)
                        s_idx_to_r_idx[target_idx] = r_idx
                tuple_graph_ext = TupleGraphExtFactory().make_tuple_graph_ext(tg, instance_data.transition_system, s_idx_to_r_idx, r_idx_to_s_idxs)
                tuple_graph_ext_by_state_index.append(tuple_graph_ext)
            instance_datas_ext.append(InstanceDataExt(tuple_graph_ext_by_state_index))
        assert count_state_pairs >= len(rules)
        print(f"Num state pairs: {count_state_pairs}")
        print(f"Num rules: {len(rules)}")
        return EquivalenceData(rules, instance_datas_ext)

    def _make_conditions(self, policy_builder: dlplan.PolicyBuilder, source_idx: int, policy_boolean_features, policy_numerical_features, instance_feature_data):
        """ Create conditions over all features that are satisfied in source_idx """
        conditions = []
        numerical_feature_valuations = instance_feature_data.numerical_feature_valuations
        boolean_feature_valuations = instance_feature_data.boolean_feature_valuations
        for n_idx in range(len(policy_numerical_features)):
            if numerical_feature_valuations[source_idx][n_idx] > 0:
                conditions.append(policy_builder.add_gt_condition(policy_numerical_features[n_idx]))
            else:
                conditions.append(policy_builder.add_eq_condition(policy_numerical_features[n_idx]))
        for b_idx in range(len(policy_boolean_features)):
            if boolean_feature_valuations[source_idx][b_idx]:
                conditions.append(policy_builder.add_pos_condition(policy_boolean_features[b_idx]))
            else:
                conditions.append(policy_builder.add_neg_condition(policy_boolean_features[b_idx]))
        return conditions

    def _make_effects(self, policy_builder: dlplan.PolicyBuilder, source_idx: int, target_idx: int, policy_boolean_features, policy_numerical_features, instance_feature_data):
        """ Create effects over all features that are satisfied in (source_idx,target_idx) """
        effects = []
        numerical_feature_valuations = instance_feature_data.numerical_feature_valuations
        boolean_feature_valuations = instance_feature_data.boolean_feature_valuations
        for n_idx in range(len(policy_numerical_features)):
            if instance_feature_data.numerical_feature_valuations[source_idx][n_idx] > numerical_feature_valuations[target_idx][n_idx]:
                effects.append(policy_builder.add_dec_effect(policy_numerical_features[n_idx]))
            elif numerical_feature_valuations[source_idx][n_idx] < numerical_feature_valuations[target_idx][n_idx]:
                effects.append(policy_builder.add_inc_effect(policy_numerical_features[n_idx]))
            else:
                effects.append(policy_builder.add_bot_effect(policy_numerical_features[n_idx]))
        for b_idx in range(len(policy_boolean_features)):
            if boolean_feature_valuations[source_idx][b_idx] and not boolean_feature_valuations[target_idx][b_idx]:
                effects.append(policy_builder.add_neg_effect(policy_boolean_features[b_idx]))
            elif not boolean_feature_valuations[source_idx][b_idx] and boolean_feature_valuations[target_idx][b_idx]:
                effects.append(policy_builder.add_pos_effect(policy_boolean_features[b_idx]))
            else:
                effects.append(policy_builder.add_bot_effect(policy_boolean_features[b_idx]))
        return effects
