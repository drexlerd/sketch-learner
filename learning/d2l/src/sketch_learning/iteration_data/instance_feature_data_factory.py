from typing import  List,  Tuple

from .domain_feature_data import DomainFeatureData
from .instance_feature_data import InstanceFeatureData

from ..instance_data.instance_data import InstanceData


class InstanceFeatureDataFactory:
    def make_instance_feature_data(self, instance_data: InstanceData, domain_feature_data: DomainFeatureData) -> Tuple[DomainFeatureData, List[InstanceFeatureData]]:
        boolean_feature_valuations = dict()
        numerical_feature_valuations = dict()
        initial_dlplan_state = instance_data.transition_system.s_idx_to_dlplan_state[instance_data.transition_system.initial_s_idx]
        #print([atom.get_name() for atom in instance_data.instance_info.get_static_atoms()])
        for s_idx, dlplan_state in instance_data.transition_system.s_idx_to_dlplan_state.items():
            #print(s_idx, str(dlplan_state))
            b_per_state = []
            for boolean_feature in domain_feature_data.boolean_features:
                b_per_state.append(boolean_feature.evaluate_seed(initial_dlplan_state, dlplan_state))
            boolean_feature_valuations[s_idx] = b_per_state
            n_per_state = []
            for numerical_feature in domain_feature_data.numerical_features:
                n_per_state.append(numerical_feature.evaluate_seed(initial_dlplan_state, dlplan_state))
            numerical_feature_valuations[s_idx] = n_per_state
            #print(n_per_state)
        return InstanceFeatureData(boolean_feature_valuations, numerical_feature_valuations)
