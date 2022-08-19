from typing import List
from dataclasses import dataclass

from ..instance_data.subproblem import SubproblemData


@dataclass
class StatePair:
    source_idx: int
    target_idx: int

    def __eq__(self, other):
        return self.source_idx == other.source_idx and self.target_idx == other.target_idx

    def __hash__(self):
        return hash((self.source_idx, self.target_idx))


@dataclass
class StatePairData:
    """
    StatePairData contains:
        (1) all state pairs for that can be pi-compatible, and
        (2) all states that are part of a state pair in (1)

    This allows a common interface for computing sketches or policies.
    The reason is that we do not care about the transition labels
    and just the state pair.
    """
    state_pairs: List[StatePair]
