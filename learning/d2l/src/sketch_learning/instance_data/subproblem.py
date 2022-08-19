from dataclasses import dataclass
from typing import Dict, MutableSet

from .instance_data import InstanceData


@dataclass
class Transition:
    source_idx: int
    target_idx: int
    optimal: bool

    def __eq__(self, other):
        return self.source_idx == other.source_idx and self.target_idx == other.target_idx and self.optimal == other.optimal

    def __hash__(self):
        return hash((self.source_idx, self.target_idx, self.optimal))


@dataclass
class SubproblemData:
    id: int
    instance_data: InstanceData
    root_idx: int
    forward_transitions: Dict[int, MutableSet[Transition]]
    expanded_states: MutableSet[int]
    generated_states: MutableSet[int]

    def print(self):
        print("Subproblem:")
        print("    Root index:", self.root_idx)
        print("    Forward transitions:", self.forward_transitions)
        print("    Expanded states:", self.expanded_states)
        print("    Generated states:", self.generated_states)
