from operator import ge
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
class StateEquivalenceData:
    t_idx_to_rule_idxs: Dict[int, MutableSet[int]]
    rule_idx_to_deadend_distance: Dict[int, int]

    def print(self):
        print("State equivalence data:")
        print(f"    t_idx_to_rule_idxs: {self.t_idx_to_rule_idxs}")
        print(f"    rule_idx_to_deadend_distance: {self.rule_idx_to_deadend_distance}")


@dataclass
class InstanceEquivalenceData:
    rules: List[dlplan.Rule]
    s_idx_to_state_equivalence_datas: Dict[int, StateEquivalenceData]

    def print(self):
        print("Instance equivalence data:")
        print(f"    rules: {self.rules}")
        for state_equivalence_data in self.s_idx_to_state_equivalence_datas.values():
            state_equivalence_data.print()


class EquivalenceDataFactory:
    def make_equivalence_class_data(self, instance_datas: List[InstanceData], domain_feature_data: DomainFeatureData, instance_feature_datas: List[InstanceFeatureData]):
        policy_builder = dlplan.PolicyBuilder()
        boolean_features = domain_feature_data.boolean_features
        numerical_features = domain_feature_data.numerical_features
        policy_boolean_features = [policy_builder.add_boolean_feature(b) for b in boolean_features]
        policy_numerical_features = [policy_builder.add_numerical_feature(n) for n in numerical_features]
        rules = []
        rule_repr_to_idx = dict()
        instance_equivalence_datas = []
        for instance_data, instance_feature_data in zip(instance_datas, instance_feature_datas):
            rule_idx_to_state_pairs = defaultdict(list)
            state_pair_to_rule_idx = dict()
            state_to_rule_idxs = defaultdict(set)
            numerical_feature_valuations = instance_feature_data.numerical_feature_valuations
            boolean_feature_valuations = instance_feature_data.boolean_feature_valuations
            count_state_pairs = 0
            s_idx_to_state_equivalence_datas = dict()
            for tg in instance_data.tuple_graphs_by_state_index:
                if tg is None:
                    continue
                source_idx = tg.root_idx
                t_idx_to_rule_idxs = defaultdict(set)
                rule_idx_to_deadend_distance = dict()
                if tg.width == 0:
                    low = 1
                else:
                    low = 0
                for s_idxs in tg.s_idxs_by_distance:
                    for target_idx in s_idxs:
                        # add conditions
                        conditions = []
                        for n_idx in range(len(numerical_features)):
                            if numerical_feature_valuations[source_idx][n_idx] > 0:
                                conditions.append(policy_builder.add_gt_condition(policy_numerical_features[n_idx]))
                            else:
                                conditions.append(policy_builder.add_eq_condition(policy_numerical_features[n_idx]))
                        for b_idx in range(len(boolean_features)):
                            if boolean_feature_valuations[source_idx][b_idx]:
                                conditions.append(policy_builder.add_pos_condition(policy_boolean_features[b_idx]))
                            else:
                                conditions.append(policy_builder.add_neg_condition(policy_boolean_features[b_idx]))
                        effects = []
                        for n_idx in range(len(numerical_features)):
                            if numerical_feature_valuations[source_idx][n_idx] > numerical_feature_valuations[target_idx][n_idx]:
                                effects.append(policy_builder.add_dec_effect(policy_numerical_features[n_idx]))
                            elif numerical_feature_valuations[source_idx][n_idx] < numerical_feature_valuations[target_idx][n_idx]:
                                effects.append(policy_builder.add_inc_effect(policy_numerical_features[n_idx]))
                            else:
                                effects.append(policy_builder.add_bot_effect(policy_numerical_features[n_idx]))
                        for b_idx in range(len(boolean_features)):
                            if boolean_feature_valuations[source_idx][b_idx] and not boolean_feature_valuations[target_idx][b_idx]:
                                effects.append(policy_builder.add_neg_effect(policy_boolean_features[b_idx]))
                            elif not boolean_feature_valuations[source_idx][b_idx] and boolean_feature_valuations[target_idx][b_idx]:
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
                        print(source_idx)
                        print(tg.s_idx_to_t_idxs)
                        for t_idx in tg.s_idx_to_t_idxs[source_idx]:
                            t_idx_to_rule_idxs[t_idx].add(rule_idx)
                        if instance_data.transition_system.is_deadend(target_idx):
                            rule_deadend_distance = rule_idx_to_deadend_distance.get(rule_idx, math.inf)
                            rule_idx_to_deadend_distance[rule_idx] = min( rule_deadend_distance)

                        state_pair = (source_idx, target_idx)
                        rule_idx_to_state_pairs[rule_idx].append(state_pair)
                        state_pair_to_rule_idx[state_pair] = rule_idx
                        state_to_rule_idxs[source_idx].add(rule_idx)
                        count_state_pairs += 1
                s_idx_to_state_equivalence_datas[source_idx] = StateEquivalenceData(t_idx_to_rule_idxs, rule_idx_to_deadend_distance)
            print(f"Finished computing equivalence classes.")
            print(f"Num state pairs: {count_state_pairs}")
            print(f"Num equivalence classes: {len(rules)}")
            instance_equivalence_datas.append(InstanceEquivalenceData(rules, s_idx_to_state_equivalence_datas))
            instance_equivalence_datas[-1].print()
        return rules, instance_equivalence_datas