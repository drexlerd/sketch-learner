from enum import Enum
from typing import Dict, Tuple

from .state_pair import StatePair


class StatePairClassification(Enum):
    BAD = -1
    DONTCARE = 0
    GOOD = 1


class StatePairClassifier:
    def __init__(self, state_pair_classification: Dict[int, StatePairClassification]):
        self.state_pair_to_classification = state_pair_classification

    def classify(self, state_pair: StatePair):
        return self.state_pair_to_classification[state_pair]
