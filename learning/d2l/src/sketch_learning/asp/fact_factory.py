import clingo

from typing import List
from dataclasses import dataclass

from ..instance_data.instance_data import InstanceData
from ..iteration_data.feature_data import FeatureData
from ..instance_data.tuple_graph import TupleGraph
from ..instance_data.transition_system import TransitionSystem
from .instance_builder import ASPInstanceBuilder


class ASPFactFactory:
    def make_asp_facts(self, instance_datas: List[InstanceData], feature_data: FeatureData):
        builder = ASPInstanceBuilder()
        self._add_domain_facts(builder, feature_data)
        for i in range(len(instance_datas)):
            self._add_instance_facts(i, builder, instance_datas[i], feature_data)
        return str(builder)

    def _add_domain_facts(self, builder: ASPInstanceBuilder, feature_data: FeatureData):
        f_idx = 0
        for boolean in feature_data.boolean_features:
            builder.add_boolean_feature(f_idx, boolean.compute_complexity())
            f_idx += 1
        for numerical in feature_data.numerical_features:
            builder.add_numerical_feature(f_idx, numerical.compute_complexity())
            f_idx += 1

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
            distance = 1
            for t_idxs in tuple_graph.t_idxs_by_distance[1:]:
                for t_idx in t_idxs:
                    builder.add_tuple_distance(instance_idx, root_state_idx, t_idx, distance)
                    builder.add_tuple(instance_idx, root_state_idx, t_idx)
                    for s_idx in tuple_graph.t_idx_to_s_idxs[t_idx]:
                        builder.add_contain(instance_idx, root_state_idx, s_idx, t_idx)
                distance += 1
            # We include (root_idx,root_idx,0) s.t. the asp constraints disallow self loops of the sketch in the training instances.
            assert [root_state_idx] == tuple_graph.s_idxs_by_distance[0]
            if tuple_graph.width == 0:
                low = 1
            else:
                low = 0
            for d in range(low, len(tuple_graph.s_idxs_by_distance)):
                for target_idx in tuple_graph.s_idxs_by_distance[d]:
                    builder.add_state_distance(instance_idx, root_state_idx, target_idx, d)

    def _add_feature_data_facts(self, instance_idx: int, builder: ASPInstanceBuilder, feature_data: FeatureData):
        for s_idx in range(len(feature_data.boolean_feature_valuations[instance_idx])):
            f_idx = 0
            for boolean_feature_valuation in feature_data.boolean_feature_valuations[instance_idx][s_idx]:
                builder.add_boolean_feature_valuation(instance_idx, f_idx, s_idx, boolean_feature_valuation)
                f_idx += 1
            for numerical_feature_valuation in feature_data.numerical_feature_valuations[instance_idx][s_idx]:
                builder.add_numerical_feature_valuation(instance_idx, f_idx, s_idx, numerical_feature_valuation)
                f_idx += 1
