from enum import Enum
from typing import Dict, Tuple

from .state_pair import StatePair


class StatePairClassification(Enum):
    DELTA_OPTIMAL = 0
    NOT_DELTA_OPTIMAL = 1


class StatePairClassifier:
    def __init__(self, delta, state_pair_classification: Dict[StatePair, StatePairClassification]):
        self.delta = delta
        self.state_pair_to_classification = state_pair_classification
        self.expanded_states = None # DELTA_OPTIMAL reachable with outgoing DELTA_OPTIMAL
        self.generated_states = None # DELTA_OPTIMAL reachable

    def classify(self, state_pair: StatePair):
        return self.state_pair_to_classification[state_pair]
