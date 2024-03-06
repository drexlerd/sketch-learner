from pymimir import State, Action
from dataclasses import dataclass
from typing import List


@dataclass
class CreatingInfo:
    parent_state: State
    creating_action: Action


@dataclass
class SearchNode:
    creating_infos: List[CreatingInfo]
