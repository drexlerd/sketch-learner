from typing import List, Dict, Union

from .iteration_data import IterationData

from ..preprocessing import PreprocessingData


def compute_per_state_feature_valuations(
        preprocessing_data: PreprocessingData,
        iteration_data: IterationData) -> None:
    """ Evaluate features on representative concrete state of all global faithful abstract states.
    """
    gfa_state_id_to_feature_evaluations: Dict[int, List[Union[bool, int]]] = dict()
    for gfa_state in iteration_data.gfa_states:
        instance_idx = gfa_state.get_abstraction_index()
        instance_data = preprocessing_data.instance_datas[instance_idx]
        dlplan_ss_state = preprocessing_data.state_finder.get_dlplan_ss_state(gfa_state)
        global_state_id = gfa_state.get_id()
        state_feature_valuations: List[Union[bool, int]] = []
        for feature in iteration_data.feature_pool:
            state_feature_valuations.append(feature.dlplan_feature.evaluate(dlplan_ss_state, instance_data.denotations_caches))
        gfa_state_id_to_feature_evaluations[global_state_id] = state_feature_valuations

    return gfa_state_id_to_feature_evaluations