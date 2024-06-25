from typing import List, Dict, Union

import pymimir as mm

from ..iteration_data.iteration_data import IterationData
from ..instance_data.instance_data import InstanceData
from ..domain_data.domain_data import DomainData
from ..preprocessing_data.state_finder import StateFinder


def compute_per_state_feature_valuations(
        domain_data: DomainData,
        instance_datas: List[InstanceData],
        iteration_data: IterationData,
        gfa_state_id_to_tuple_graph: Dict[int, mm.TupleGraph],
        state_finder: StateFinder) -> None:
    """ Evaluate features on representative concrete state of all global faithful abstract states.
    """
    gfa_state_id_to_feature_evaluations: Dict[int, List[Union[bool, int]]] = dict()
    for gfa_state in iteration_data.gfa_states:
        instance_idx = gfa_state.get_abstraction_index()
        instance_data = instance_datas[instance_idx]
        dlplan_ss_state = state_finder.get_dlplan_ss_state(gfa_state)
        global_state_id = gfa_state.get_id()
        state_feature_valuations: List[Union[bool, int]] = []
        for feature in iteration_data.feature_pool:
            state_feature_valuations.append(feature.dlplan_feature.evaluate(dlplan_ss_state, instance_data.denotations_caches))
        gfa_state_id_to_feature_evaluations[global_state_id] = state_feature_valuations

    return gfa_state_id_to_feature_evaluations