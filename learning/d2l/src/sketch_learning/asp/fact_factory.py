import clingo
import re

from typing import List
from dataclasses import dataclass

from ..instance_data.instance_data import InstanceData
from ..iteration_data.feature_data import DomainFeatureData, InstanceFeatureData
from ..iteration_data.equivalence_data import RuleEquivalenceData, StatePairEquivalenceData, TupleGraphEquivalenceData

from .facts.iteration_data.domain_feature_data import DomainFeatureDataFactFactory
from .facts.iteration_data.equivalence_data import EquivalenceDataFactFactory
from .facts.instance_data.tuple_graph import TupleGraphFactFactory
from .facts.instance_data.transition_system import TransitionSystemFactFactory


class ASPFactFactory:
    def make_asp_facts(self, instance_datas: List[InstanceData], domain_feature_data: DomainFeatureData, rule_equivalence_data: RuleEquivalenceData, instance_state_pair_equivalence_datas: List[StatePairEquivalenceData], instance_tuple_graph_equivalence_datas: List[TupleGraphEquivalenceData]):
        facts = []
        facts.extend(DomainFeatureDataFactFactory().make_facts(domain_feature_data))
        facts.extend(EquivalenceDataFactFactory().make_facts(rule_equivalence_data, domain_feature_data))
        for instance_idx, (instance_data, instance_state_pair_equivalence_data, instance_tuple_graph_equivalence_data) in enumerate(zip(instance_datas, instance_state_pair_equivalence_datas, instance_tuple_graph_equivalence_datas)):
            facts.extend(TransitionSystemFactFactory().make_facts(instance_idx, instance_data.transition_system))
            for tuple_graph, tuple_graph_equivalence_data in zip(instance_data.tuple_graphs_by_state_index, instance_tuple_graph_equivalence_data):
                facts.extend(TupleGraphFactFactory().make_facts(instance_idx, tuple_graph, instance_state_pair_equivalence_data, tuple_graph_equivalence_data))
        return sorted(facts)
