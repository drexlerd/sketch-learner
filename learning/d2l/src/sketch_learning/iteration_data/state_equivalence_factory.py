import dlplan

from collections import defaultdict
from dataclasses import dataclass
from typing import List

from sketch_learning.iteration_data.state_equivalence import InstanceStateEquivalence, DomainStateEquivalence

from .domain_feature_data import DomainFeatureData

from ..instance_data.instance_data import InstanceData


@dataclass
class StatePairEquivalenceStatistics:
    num_equivalences: int = 0
    num_states: int = 0

    def increment_num_states(self):
        self.num_states += 1

    def increment_num_equivalences(self):
        self.num_equivalences += 1

    def print(self):
        print("StatePairEquivalenceStatistics:")
        print("    num_states:", self.num_states)
        print("    num_equivalences:", self.num_equivalences)


class StateEquivalenceFactory:
    def __init__(self):
        self.statistics = StatePairEquivalenceStatistics()

    def make_state_equivalences(self, domain_feature_data: DomainFeatureData, instance_datas: List[InstanceData]):
        feature_valuation_to_state_class_idx = dict()
        for instance_data in instance_datas:
            s_idx_to_state_class_idx = dict()
            state_class_idx_to_s_idxs = defaultdict(set)
            for s_idx in instance_data.state_space.get_state_indices():
                self.statistics.increment_num_states()
                feature_valuation = instance_data.feature_valuations[s_idx]
                # if feature valuation has not been seen before then assign next index
                if feature_valuation not in feature_valuation_to_state_class_idx:
                    self.statistics.increment_num_equivalences()
                    feature_valuation_to_state_class_idx[feature_valuation] = len(feature_valuation_to_state_class_idx)
                state_class_idx = feature_valuation_to_state_class_idx[feature_valuation]
                s_idx_to_state_class_idx[s_idx] = state_class_idx
                state_class_idx_to_s_idxs[state_class_idx].add(s_idx)
            instance_data.state_equivalence = InstanceStateEquivalence(s_idx_to_state_class_idx, state_class_idx_to_s_idxs)
        goal_state_class_idxs = set()
        nongoal_state_class_idxs = set()
        mixed_state_class_idxs = set()
        for state_class_idx in feature_valuation_to_state_class_idx.values():
            if all([instance_data.goal_distance_information.is_goal(s_idx) for instance_data in instance_datas for s_idx in instance_data.state_equivalence.state_class_idx_to_s_idxs[state_class_idx]]):
                goal_state_class_idxs.add(state_class_idx)
            elif all([instance_data.goal_distance_information.is_nongoal(s_idx) for instance_data in instance_datas for s_idx in instance_data.state_equivalence.state_class_idx_to_s_idxs[state_class_idx]]):
                nongoal_state_class_idxs.add(state_class_idx)
            else:
                mixed_state_class_idxs.add(state_class_idx)
        # we want goal separating features
        assert not mixed_state_class_idxs
        return DomainStateEquivalence(
            feature_valuation_to_state_class_idx,
            goal_state_class_idxs,
            nongoal_state_class_idxs,
            mixed_state_class_idxs)
