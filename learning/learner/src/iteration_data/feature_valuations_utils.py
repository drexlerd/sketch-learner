from typing import List

from learner.src.iteration_data.feature_valuations import FeatureValuations, PerStateFeatureValuations
from learner.src.instance_data.instance_data import InstanceData


def compute_per_state_feature_valuations(instance_datas: List[InstanceData]) -> None:
    """ Evaluates the features on all states.
    """
    for instance_data in instance_datas:
        per_state_feature_valuations = PerStateFeatureValuations()
        for s_idx, dlplan_state in instance_data.state_space.get_states().items():
            feature_valuations = FeatureValuations()
            for b_idx, boolean_feature in instance_data.domain_data.feature_pool.boolean_features.f_idx_to_feature.items():
                valuation = boolean_feature.dlplan_feature.evaluate(dlplan_state, instance_data.denotations_caches)
                feature_valuations.b_idx_to_val[b_idx] = valuation
            for n_idx, numerical_feature in instance_data.domain_data.feature_pool.numerical_features.f_idx_to_feature.items():
                valuation = numerical_feature.dlplan_feature.evaluate(dlplan_state, instance_data.denotations_caches)
                feature_valuations.n_idx_to_val[n_idx] = valuation
            per_state_feature_valuations.s_idx_to_feature_valuations[s_idx] = feature_valuations
        instance_data.set_per_state_feature_valuations(per_state_feature_valuations)
