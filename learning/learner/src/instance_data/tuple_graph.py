from dataclasses import dataclass, field
from typing import Dict

import pymimir as mm


@dataclass
class PerStateTupleGraphs:
    s_idx_to_tuple_graph: Dict[int, mm.TupleGraph] = field(default_factory=dict)
