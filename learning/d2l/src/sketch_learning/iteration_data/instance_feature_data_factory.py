from typing import  List,  Tuple

from .domain_feature_data import DomainFeatureData
from .instance_feature_data import InstanceFeatureData

from ..instance_data.instance_data import InstanceData


class InstanceFeatureDataFactory:
    def make_instance_feature_data(self, instance_data: InstanceData, domain_feature_data: DomainFeatureData) -> Tuple[DomainFeatureData, List[InstanceFeatureData]]:
        boolean_feature_valuations = dict()
        numerical_feature_valuations = dict()
        for s_idx, dlplan_state in enumerate(instance_data.transition_system.states_by_index):
            b_per_state = []
            for boolean_feature in domain_feature_data.boolean_features:
                b_per_state.append(boolean_feature.evaluate(dlplan_state))
            boolean_feature_valuations[s_idx] = b_per_state
            n_per_state = []
            for numerical_feature in domain_feature_data.numerical_features:
                n_per_state.append(numerical_feature.evaluate(dlplan_state))
            numerical_feature_valuations[s_idx] = n_per_state
        return InstanceFeatureData(boolean_feature_valuations, numerical_feature_valuations)
