from enum import Enum
from typing import Dict, List, MutableSet

from .state_pair import StatePair


class StatePairClassification(Enum):
    DELTA_OPTIMAL = 0
    NOT_DELTA_OPTIMAL = 1


class StatePairClassifier:
    """ """
    def __init__(self, delta, state_pair_to_classification: Dict[StatePair, StatePairClassification], source_idx_to_state_pairs: Dict[int, MutableSet[StatePair]], expanded_state_indices: List[int], generated_state_indices: List[int]):
        self.delta = delta
        self.state_pair_to_classification = state_pair_to_classification
        self.source_idx_to_state_pairs = source_idx_to_state_pairs
        self.expanded_state_indices = expanded_state_indices
        self.generated_state_indices = generated_state_indices


    def classify(self, state_pair: StatePair):
        return self.state_pair_to_classification[state_pair]

    def print(self):
        print("StatePairClassifier:")
        print("    state_pair_to_classification:", self.state_pair_to_classification)
        print("    source_idx_to_state_pairs:", self.source_idx_to_state_pairs)
        print("    expanded_state_indices:", self.expanded_state_indices)
        print("    generated_state_indices:", self.generated_state_indices)
