from typing import List

from .feature_valuations import FeatureValuations, PerStateFeatureValuations

from ..instance_data.instance_data import InstanceData
from ..domain_data.domain_data import DomainData


def compute_per_state_feature_valuations(instance_datas: List[InstanceData], domain_data: DomainData) -> None:
    """ Evaluates the features on all states.
    """
    for instance_data in instance_datas:
        per_state_feature_valuations = PerStateFeatureValuations()
        for s_idx, dlplan_state in instance_data.state_space.get_states().items():
            state_feature_valuations = FeatureValuations()
            for feature in instance_data.domain_data.feature_pool.features:
                state_feature_valuations.feature_valuations.append(feature.dlplan_feature.evaluate(dlplan_state, instance_data.denotations_caches))
            per_state_feature_valuations.s_idx_to_feature_valuations[s_idx] = state_feature_valuations
        instance_data.per_state_feature_valuations = per_state_feature_valuations
