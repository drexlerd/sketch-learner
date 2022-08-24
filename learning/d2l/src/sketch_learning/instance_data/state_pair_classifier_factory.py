import math

from enum import Enum
from typing import List, Dict, Tuple

from .instance_data import InstanceData
from .state_pair import StatePair
from .state_pair_classifier import StatePairClassification, StatePairClassifier


class StatePairClassifierFactory:
    def __init__(self, delta=1.0):
        assert delta >= 1
        self.delta = delta

    def make_state_pair_classifier(self, instance_data: InstanceData, state_pairs: List[StatePair]):
        transition_system = instance_data.transition_system
        _, goal_distances = transition_system.partition_states_by_distance(instance_data.transition_system.goals, forward=False, stop_upon_goal=False)
        for state_pair in state_pairs:
            if self.delta * goal_distances.get(state_pair.source_idx, math.inf) < goal_distances.get(state_pair.target_idx, math.inf) + state_pair.distance:
                # NOT_DELTA_OPTIMAL
                pass
            else:
                # DELTA_OPTIMAL
                pass
