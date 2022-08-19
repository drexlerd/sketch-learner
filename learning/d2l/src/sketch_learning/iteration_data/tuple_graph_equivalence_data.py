from typing import Dict, List, MutableSet
from dataclasses import dataclass

from .tuple_graph_equivalence import TupleGraphEquivalence

@dataclass
class TupleGraphEquivalenceData:
    tuple_graph_equivalence_by_state_index: List[TupleGraphEquivalence]
