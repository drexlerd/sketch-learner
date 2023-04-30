from typing import Dict

from learner.src.instance_data.instance_data import InstanceData
from learner.src.iteration_data.feature_valuations import FeatureValuation


class FeatureValuationsFactory:
    def make_feature_valuations(self, instance_data: InstanceData) -> Dict[int, FeatureValuation]:
        feature_valuations = dict()
        for s_idx, dlplan_state in instance_data.state_space.get_states().items():
            boolean_state_feature_valuations = []
            # print(instance_data.state_information.get_state(s_idx))
            for boolean_feature in instance_data.domain_data.domain_feature_data.boolean_features.features_by_index:
                boolean_state_feature_valuations.append(boolean_feature.dlplan_feature.evaluate(dlplan_state))
                # print(boolean_feature.dlplan_feature.evaluate(dlplan_state), boolean_feature.dlplan_feature.compute_repr())
            numerical_state_feature_valuations = []
            for numerical_feature in instance_data.domain_data.domain_feature_data.numerical_features.features_by_index:
                numerical_state_feature_valuations.append(numerical_feature.dlplan_feature.evaluate(dlplan_state))
                # print(numerical_feature.dlplan_feature.evaluate(dlplan_state), numerical_feature.dlplan_feature.compute_repr())
            feature_valuations[s_idx] = FeatureValuation(s_idx, boolean_state_feature_valuations, numerical_state_feature_valuations)
        return feature_valuations
