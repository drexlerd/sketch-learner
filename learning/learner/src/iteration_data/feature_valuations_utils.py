from typing import List, Dict, Union

from ..instance_data.instance_data import InstanceData, StateFinder
from ..domain_data.domain_data import DomainData


def compute_per_state_feature_valuations(instance_datas: List[InstanceData], domain_data: DomainData, state_finder: StateFinder) -> None:
    """ Evaluate features on representative concrete state of all global faithful abstract states.
    """
    gfa_state_id_to_feature_evaluations: Dict[int, List[Union[bool, int]]] = dict()
    for gfa_state in domain_data.gfa_states:
        new_instance_idx = domain_data.instance_idx_remap[gfa_state.get_abstraction_id()]
        dlplan_ss_state = state_finder.get_dlplan_ss_state(gfa_state)
        global_state_id = gfa_state.get_id()
        state_feature_valuations: List[Union[bool, int]] = []
        for feature in domain_data.feature_pool.features:
            state_feature_valuations.append(feature.dlplan_feature.evaluate(dlplan_ss_state, instance_datas[new_instance_idx].denotations_caches))
        gfa_state_id_to_feature_evaluations[global_state_id] = state_feature_valuations
    domain_data.gfa_state_id_to_feature_evaluations = gfa_state_id_to_feature_evaluations