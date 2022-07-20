import clingo
import re

from typing import List
from dataclasses import dataclass

from ..instance_data.instance_data import InstanceData
from ..iteration_data.feature_data import DomainFeatureData, InstanceFeatureData
from ..iteration_data.equivalence_data import EquivalenceData, InstanceDataExt, TupleGraphExt

from .facts.iteration_data.domain_feature_data import DomainFeatureDataFactFactory
from .facts.iteration_data.equivalence_data import EquivalenceDataFactFactory
from .facts.instance_data.tuple_graph import TupleGraphFactFactory
from .facts.instance_data.transition_system import TransitionSystemFactFactory


class ASPFactFactory:
    def make_asp_facts(self, instance_datas: List[InstanceData], domain_feature_data: DomainFeatureData, instance_feature_datas: List[InstanceFeatureData], equivalence_data: EquivalenceData):
        facts = []
        facts.extend(DomainFeatureDataFactFactory().make_facts(domain_feature_data))
        facts.extend(EquivalenceDataFactFactory().make_facts(equivalence_data, domain_feature_data))
        for instance_idx, instance_data in enumerate(instance_datas):
            facts.extend(TransitionSystemFactFactory().make_facts(instance_idx, instance_data.transition_system))
            for tuple_graph_ext in equivalence_data.instance_data_exts[instance_idx].tuple_graph_ext_by_state_index:
                facts.extend(TupleGraphFactFactory().make_facts(instance_idx, tuple_graph_ext))
        return sorted(facts)
