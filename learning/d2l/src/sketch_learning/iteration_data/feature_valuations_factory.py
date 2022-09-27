from typing import  List,  Tuple

from .domain_feature_data import DomainFeatureData
from .feature_valuations import FeatureValuation

from ..instance_data.instance_data import InstanceData


class FeatureValuationsFactory:
    def make_feature_valuations(self, instance_data: InstanceData, domain_feature_data: DomainFeatureData) -> List[FeatureValuation]:
        feature_valuations = dict()
        for s_idx in instance_data.state_space.get_state_indices():
            dlplan_state = instance_data.state_information.get_state(s_idx)
            boolean_state_feature_valuations = []
            for boolean_feature in domain_feature_data.boolean_features:
                boolean_state_feature_valuations.append(boolean_feature.evaluate(dlplan_state))
            numerical_state_feature_valuations = []
            for numerical_feature in domain_feature_data.numerical_features:
                numerical_state_feature_valuations.append(numerical_feature.evaluate(dlplan_state))
            feature_valuations[s_idx] = FeatureValuation(s_idx, boolean_state_feature_valuations, numerical_state_feature_valuations)
        return feature_valuations
