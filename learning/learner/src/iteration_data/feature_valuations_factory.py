from typing import Dict
from collections import defaultdict

from learner.src.instance_data.instance_data import InstanceData
from learner.src.iteration_data.feature_valuations import StateFeatureValuation


class FeatureValuationsFactory:
    def make_feature_valuations(self, instance_data: InstanceData) -> Dict[int, StateFeatureValuation]:
        """ Evaluates the features on all states.   
        """
        state_feature_valuations = dict()
        boolean_feature_valuations = defaultdict(list)
        numerical_feature_valuations = defaultdict(list)
        for s_idx, dlplan_state in instance_data.state_space.get_states().items():
            boolean_state_feature_valuations = dict()
            for b_idx, boolean_feature in instance_data.domain_data.domain_feature_data.boolean_features.f_idx_to_feature.items():
                valuation = boolean_feature.dlplan_feature.evaluate(dlplan_state, instance_data.denotations_caches)
                boolean_state_feature_valuations[b_idx] = valuation
                boolean_feature_valuations[b_idx].append(valuation)
            numerical_state_feature_valuations = dict()
            for n_idx, numerical_feature in instance_data.domain_data.domain_feature_data.numerical_features.f_idx_to_feature.items():
                valuation = numerical_feature.dlplan_feature.evaluate(dlplan_state, instance_data.denotations_caches)
                numerical_state_feature_valuations[n_idx] = valuation
                numerical_feature_valuations[n_idx].append(valuation)
            state_feature_valuations[s_idx] = StateFeatureValuation(s_idx, boolean_state_feature_valuations, numerical_state_feature_valuations)
        return state_feature_valuations, boolean_feature_valuations, numerical_feature_valuations
