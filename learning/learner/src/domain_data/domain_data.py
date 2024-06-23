from dataclasses import dataclass
from typing import List, Dict, Union

import pymimir as mm

from dlplan.core import VocabularyInfo, SyntacticElementFactory
from dlplan.policy import PolicyFactory, Rule

from ..iteration_data.feature_pool import Feature
from ..iteration_data.state_pair_equivalence import StatePairEquivalence
from ..iteration_data.tuple_graph_equivalence import TupleGraphEquivalence

@dataclass
class DomainData:
    """ Store data related to a domain. """

    # Persistant data.
    domain_filename: str
    vocabulary_info: VocabularyInfo
    policy_builder: PolicyFactory
    syntactic_element_factory: SyntacticElementFactory
    instance_idx_remap : List[int] = None
    gfa_state_id_to_tuple_graph : Dict[int, mm.TupleGraph] = None

    # Changes in each iterations
    gfa_states: List[mm.GlobalFaithfulAbstractState] = None

    feature_pool: List[Feature] = None
    gfa_state_id_to_feature_evaluations: Dict[int, List[Union[bool, int]]] = None

    state_pair_equivalences: List[Rule] = None
    gfa_state_id_to_state_pair_equivalence: Dict[int, StatePairEquivalence] = None

    gfa_state_id_to_tuple_graph_equivalence: Dict[int, TupleGraphEquivalence] = None
