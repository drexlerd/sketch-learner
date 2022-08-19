from dataclasses import dataclass
from typing import List

from .tuple_graph import TupleGraph


@dataclass
class TupleGraphData:
    tuple_graphs_by_state_index: List[TupleGraph]
    minimized_tuple_graphs_by_state_index: List[TupleGraph]
