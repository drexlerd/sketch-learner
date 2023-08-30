from dataclasses import dataclass, field
from typing import Dict

from dlplan.novelty import TupleGraph


@dataclass
class PerStateTupleGraphs:
    s_idx_to_tuple_graph: Dict[int, TupleGraph] = field(default_factory=dict)
