from ctypes.wintypes import tagRECT
import re
import dlplan

from typing import List
from dataclasses import dataclass

from ..instance_data.instance_data import InstanceData
from ..iteration_data.feature_data import DomainFeatureData, InstanceFeatureData
from ..iteration_data.equivalence_data import InstanceEquivalenceData
from ..instance_data.tuple_graph import TupleGraph
from ..instance_data.transition_system import TransitionSystem
from .instance_builder import ASPInstanceBuilder


def try_parse(pattern, text, r_idx, builder_function):
    result = re.findall(pattern, text)
    if result:
        builder_function(r_idx, int(result[0]))
        return True
    return False


class ASPFactFactory:
    def make_asp_facts(self, instance_datas: List[InstanceData], domain_feature_data: DomainFeatureData, instance_feature_datas: List[InstanceFeatureData], rules: List[dlplan.Rule], instance_equivalence_datas: List[InstanceEquivalenceData]):
        builder = ASPInstanceBuilder()
        self._add_domain_facts(builder, domain_feature_data, rules)
        self._add_instance_datas_facts(builder, instance_datas)
        self._add_instance_feature_datas_facts(builder, instance_feature_datas)
        self._add_instance_equivalence_datas_facts(builder, instance_equivalence_datas)
        builder.log_stats()
        return str(builder)

    def _add_domain_facts(self, builder: ASPInstanceBuilder, domain_feature_data: DomainFeatureData, rules: List[dlplan.Rule]):
        for b_idx, boolean in enumerate(domain_feature_data.boolean_features):
            builder.add_boolean_feature(b_idx, boolean.compute_complexity())
        for n_idx, numerical in enumerate(domain_feature_data.numerical_features):
            builder.add_numerical_feature(n_idx, numerical.compute_complexity())
        for r_idx, rule in enumerate(rules):
            builder.add_rule(r_idx)
            for condition in rule.get_conditions():
                condition_str = condition.str()
                if try_parse(r"\(:c_b_pos (\d+)\)", condition_str, r_idx, builder.add_c_pos): continue
                if try_parse(r"\(:c_b_neg (\d+)\)", condition_str, r_idx, builder.add_c_neg): continue
                if try_parse(r"\(:c_n_gt (\d+)\)", condition_str, r_idx, builder.add_c_gt): continue
                if try_parse(r"\(:c_n_eq (\d+)\)", condition_str, r_idx, builder.add_c_eq): continue
            for effect in rule.get_effects():
                effect_str = effect.str()
                if try_parse(r"\(:e_b_pos (\d+)\)", effect_str, r_idx, builder.add_e_pos): continue
                if try_parse(r"\(:e_b_neg (\d+)\)", effect_str, r_idx, builder.add_e_neg): continue
                if try_parse(r"\(:e_b_bot (\d+)\)", effect_str, r_idx, builder.add_e_bot): continue
                if try_parse(r"\(:e_n_inc (\d+)\)", effect_str, r_idx, builder.add_e_inc): continue
                if try_parse(r"\(:e_n_dec (\d+)\)", effect_str, r_idx, builder.add_e_dec): continue
                if try_parse(r"\(:e_n_bot (\d+)\)", effect_str, r_idx, builder.add_e_bot): continue

    def _add_instance_datas_facts(self, builder: ASPInstanceBuilder, instance_datas: List[InstanceData]):
        for instance_idx, instance_data in enumerate(instance_datas):
            for tg in instance_data.tuple_graphs_by_state_index:
                if tg is None:
                    # width is bounded or deadend
                    continue
                builder.add_exceed(instance_idx, tg.root_idx)
                for d in range(1, len(tg.t_idxs_by_distance)):
                    for t_idx in tg.t_idxs_by_distance[d]:
                        builder.add_tuple_distance(instance_idx, tg.root_idx, t_idx, d)
                        builder.add_tuple(instance_idx, tg.root_idx, t_idx)
                        for s_idx in tg.t_idx_to_s_idxs[t_idx]:
                            builder.add_contain(instance_idx, tg.root_idx, s_idx, t_idx)
                # We include (root_idx,root_idx,0) s.t. the asp constraints disallow self loops of the sketch in the training instances.
                assert [tg.root_idx] == tg.s_idxs_by_distance[0]
                if tg.width == 0:
                    low = 1  # filter transitions instead
                else:
                    low = 0
                for d in range(low, len(tg.s_idxs_by_distance)):
                    for s_idx in tg.s_idxs_by_distance[d]:
                        builder.add_state_distance(instance_idx, tg.root_idx, s_idx, d)

    def _add_instance_feature_datas_facts(self, builder: ASPInstanceBuilder, instance_feature_datas: List[InstanceFeatureData]):
        for i, instance_feature_data in enumerate(instance_feature_datas):
            pass

    def _add_instance_equivalence_datas_facts(self, builder: ASPInstanceBuilder, instance_equivalence_datas: List[InstanceEquivalenceData]):
        for i, instance_equivalence_data in enumerate(instance_equivalence_datas):
            pass

    def _add_instance_facts(self, instance_idx: int, builder: ASPInstanceBuilder, instance_data: InstanceData, feature_data: FeatureData):
        self._add_transition_system_facts(instance_idx, builder, instance_data.transition_system)
        self._add_tuple_graph_facts(instance_idx, builder, instance_data.tuple_graphs_by_state_index)
        self._add_feature_data_facts(instance_idx, builder, feature_data)

    def _add_transition_system_facts(self, instance_idx: int, builder: ASPInstanceBuilder, transition_system: TransitionSystem):
        for state_idx in range(transition_system.get_num_states()):
            if transition_system.is_deadend(state_idx):
                builder.add_unsolvable(instance_idx, state_idx)
            else:
                builder.add_solvable(instance_idx, state_idx)

    def _add_tuple_graph_facts(self, instance_idx: int, builder: ASPInstanceBuilder, tuple_graphs_by_state_index: List[TupleGraph]):
        for root_state_idx in range(len(tuple_graphs_by_state_index)):
            tuple_graph = tuple_graphs_by_state_index[root_state_idx]
            if tuple_graph is None:
                # width is bounded or deadend
                continue
            builder.add_exceed(instance_idx, root_state_idx)
            for d in range(1, len(tuple_graph.t_idxs_by_distance)):
                for t_idx in tuple_graph.t_idxs_by_distance[d]:
                    builder.add_tuple_distance(instance_idx, root_state_idx, t_idx, d)
                    builder.add_tuple(instance_idx, root_state_idx, t_idx)
                    for s_idx in tuple_graph.t_idx_to_s_idxs[t_idx]:
                        builder.add_contain(instance_idx, root_state_idx, s_idx, t_idx)
            # We include (root_idx,root_idx,0) s.t. the asp constraints disallow self loops of the sketch in the training instances.
            assert [root_state_idx] == tuple_graph.s_idxs_by_distance[0]
            if tuple_graph.width == 0:
                low = 1  # filter transitions instead
            else:
                low = 0
            for d in range(low, len(tuple_graph.s_idxs_by_distance)):
                for s_idx in tuple_graph.s_idxs_by_distance[d]:
                    builder.add_state_distance(instance_idx, root_state_idx, s_idx, d)


    def _add_feature_data_facts(self, builder: ASPInstanceBuilder, instance_feature_data: InstanceFeatureData):
        for f_idx, f_state_values in enumerate(instance_feature_data.boolean_feature_valuations):
            for f_state_value in f_state_values:
                builder.add_boolean_feature_valuation()

        for s_idx in range(len(feature_data.boolean_feature_valuations[instance_idx])):
            f_idx = 0
            for boolean_feature_valuation in feature_data.boolean_feature_valuations[instance_idx][s_idx]:
                builder.add_boolean_feature_valuation(instance_idx, f_idx, s_idx, boolean_feature_valuation)
                f_idx += 1
            for numerical_feature_valuation in feature_data.numerical_feature_valuations[instance_idx][s_idx]:
                builder.add_numerical_feature_valuation(instance_idx, f_idx, s_idx, numerical_feature_valuation)
                f_idx += 1
