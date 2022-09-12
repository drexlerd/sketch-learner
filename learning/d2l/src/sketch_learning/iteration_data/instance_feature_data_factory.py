from typing import  List,  Tuple

from .domain_feature_data import DomainFeatureData
from .instance_feature_data import InstanceFeatureData

from ..instance_data.instance_data import InstanceData


class InstanceFeatureDataFactory:
    def make_instance_feature_data(self, instance_data: InstanceData, domain_feature_data: DomainFeatureData) -> Tuple[DomainFeatureData, List[InstanceFeatureData]]:
        boolean_feature_valuations = dict()
        numerical_feature_valuations = dict()
        for dlplan_state in instance_data.state_space.get_states_ref():
            b_per_state = []
            for boolean_feature in domain_feature_data.boolean_features:
                b_per_state.append(boolean_feature.evaluate(dlplan_state))
            boolean_feature_valuations[dlplan_state.get_index()] = b_per_state
            n_per_state = []
            for numerical_feature in domain_feature_data.numerical_features:
                n_per_state.append(numerical_feature.evaluate(dlplan_state))
            numerical_feature_valuations[dlplan_state.get_index()] = n_per_state
        return InstanceFeatureData(boolean_feature_valuations, numerical_feature_valuations)
