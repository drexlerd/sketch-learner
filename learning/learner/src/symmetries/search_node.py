from pymimir import State, Action
from dataclasses import dataclass
from typing import List, Any


@dataclass
class SearchNode:
    parent_states: List[State]
    g_value: int
    equivalence_class_key: Any
