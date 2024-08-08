from typing import List, Dict, Union

from .iteration_data import IterationData

from ..preprocessing import PreprocessingData


def compute_per_state_feature_valuations(
        preprocessing_data: PreprocessingData,
        iteration_data: IterationData) -> None:
    """ Evaluate features on representative concrete state of all global faithful abstract states.
    """
    instance_idx_to_ss_idx_to_feature_valuations: Dict[int, List[List[Union[bool, int]]]] = dict()

    for instance_data in iteration_data.instance_datas:

        dlplan_ss_states = instance_data.dlplan_ss.get_states()

        ss_idx_to_feature_valuations: List[Union[bool, int]] = []

        for mimir_ss_idx in range(instance_data.mimir_ss.get_num_states()):
            dlplan_ss_state = dlplan_ss_states[mimir_ss_idx]

            feature_valuations: List[List[Union[bool, int]]] = []

            for feature in iteration_data.feature_pool:
                feature_valuations.append(feature.dlplan_feature.evaluate(dlplan_ss_state, instance_data.denotations_caches))

            ss_idx_to_feature_valuations.append(feature_valuations)

        instance_idx_to_ss_idx_to_feature_valuations[instance_data.idx] = ss_idx_to_feature_valuations

    return instance_idx_to_ss_idx_to_feature_valuations
