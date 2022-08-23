from enum import Enum
from typing import Dict, Tuple

from .state_pair import StatePair


class StatePairClassification(Enum):
    BAD = -1
    DONTCARE = 0
    GOOD = 1


class StatePairClassifierFactory:
    def make_state_pair_classifier(self, instance_data):
        pass

    def make_state_pair_classifier_from_subproblem(self, subproblem):
        pass
