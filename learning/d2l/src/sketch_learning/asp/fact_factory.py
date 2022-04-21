import clingo
import re

from typing import List
from dataclasses import dataclass

from sketch_learning.instance_data.transition_system import TransitionSystem

from ..instance_data.instance_data import InstanceData
from ..iteration_data.feature_data import FeatureData
from ..iteration_data.equivalence_data import EquivalenceData, TupleGraphExt, TerminationGraph
from .instance_builder import ASPInstanceBuilder


def try_parse(pattern, text, r_idx, index_offset, builder_function):
    result = re.findall(pattern, text)
    if result:
        builder_function(r_idx, int(result[0]) + index_offset)
        return True
    return False


class ASPFactFactory:
    def make_asp_facts(self, instance_datas: List[InstanceData], feature_data: FeatureData, equivalence_data: EquivalenceData):
        builder = ASPInstanceBuilder()
        self._add_domain_facts(builder, feature_data, equivalence_data)
        for i in range(len(instance_datas)):
            self._add_instance_facts(i, builder, instance_datas[i], feature_data, equivalence_data)
        builder.log_stats()
        return str(builder)

    def _add_domain_facts(self, builder: ASPInstanceBuilder, feature_data: FeatureData, equivalence_data: EquivalenceData):
        f_idx = 0
        for boolean in feature_data.boolean_features:
            builder.add_boolean_feature(f_idx, boolean.compute_complexity())
            f_idx += 1
        for numerical in feature_data.numerical_features:
            builder.add_numerical_feature(f_idx, numerical.compute_complexity())
            f_idx += 1
        for r_idx, rule in enumerate(equivalence_data.rules):
            builder.add_equivalence(r_idx)
            for condition in rule.get_conditions():
                condition_str = condition.str()
                if try_parse(r"\(:c_b_pos (\d+)\)", condition_str, r_idx, 0, builder.add_c_pos): continue
                if try_parse(r"\(:c_b_neg (\d+)\)", condition_str, r_idx, 0, builder.add_c_neg): continue
                if try_parse(r"\(:c_n_gt (\d+)\)", condition_str, r_idx, len(feature_data.boolean_features), builder.add_c_gt): continue
                if try_parse(r"\(:c_n_eq (\d+)\)", condition_str, r_idx, len(feature_data.boolean_features), builder.add_c_eq): continue
            for effect in rule.get_effects():
                effect_str = effect.str()
                if try_parse(r"\(:e_b_pos (\d+)\)", effect_str, r_idx, 0, builder.add_e_pos): continue
                if try_parse(r"\(:e_b_neg (\d+)\)", effect_str, r_idx, 0, builder.add_e_neg): continue
                if try_parse(r"\(:e_b_bot (\d+)\)", effect_str, r_idx, 0, builder.add_e_bot): continue
                if try_parse(r"\(:e_n_inc (\d+)\)", effect_str, r_idx, len(feature_data.boolean_features), builder.add_e_inc): continue
                if try_parse(r"\(:e_n_dec (\d+)\)", effect_str, r_idx, len(feature_data.boolean_features), builder.add_e_dec): continue
                if try_parse(r"\(:e_n_bot (\d+)\)", effect_str, r_idx, len(feature_data.boolean_features), builder.add_e_bot): continue

    def _add_instance_facts(self, instance_idx: int, builder: ASPInstanceBuilder, instance_data: InstanceData, feature_data: FeatureData, equivalence_data: EquivalenceData):
        self._add_tuple_graph_facts(instance_idx, builder, equivalence_data.instance_datas_ext[instance_idx].tuple_graph_ext_by_state_index)
        self._add_termination_graph_facts(instance_idx, builder, equivalence_data.instance_datas_ext[instance_idx].termination_graph)
        self._add_transition_system_facts(instance_idx, builder, instance_data.transition_system)

    def _add_tuple_graph_facts(self, instance_idx: int, builder: ASPInstanceBuilder, tuple_graphs_by_state_index: List[TupleGraphExt]):
        for root_idx in range(len(tuple_graphs_by_state_index)):
            tuple_graph = tuple_graphs_by_state_index[root_idx]
            if tuple_graph is None:
                # width is bounded or deadend
                continue
            builder.add_exceed(instance_idx, root_idx)
            d = 1
            for t_idxs in tuple_graph.t_idxs_by_distance[d:]:
                for t_idx in t_idxs:
                    builder.add_tuple_distance(instance_idx, root_idx, t_idx, d)
                    builder.add_tuple(instance_idx, root_idx, t_idx)
                    for r_idx in tuple_graph.t_idx_to_r_idxs[t_idx]:
                        builder.add_contain(instance_idx, root_idx, t_idx, r_idx)
                d += 1
            for r_idx, d in tuple_graph.r_idx_to_deadend_distance.items():
                builder.add_deadend_distance(instance_idx, root_idx, r_idx, d)

    def _add_termination_graph_facts(self, instance_idx: int, builder: ASPInstanceBuilder, termination_graph: TerminationGraph):
        for r_idx, state_pairs in termination_graph.rule_idx_to_state_pairs.items():
            for state_pair in state_pairs:
                builder.add_equivalence_contains(instance_idx, r_idx, state_pair[0], state_pair[1])

    def _add_transition_system_facts(self, instance_idx: int, builder: ASPInstanceBuilder, transition_system: TransitionSystem):
        for s_idx in range(transition_system.get_num_states()):
            if not transition_system.is_deadend(s_idx):
                builder.add_solvable(instance_idx, s_idx)
