from clingo import Control, Number, Symbol

from collections import defaultdict
from typing import List

from .asp_factory import ASPFactory

from ..instance_data.instance_data import InstanceData
from ..instance_data.tuple_graph import TupleGraph
from ..instance_data.state_pair_classifier import StatePairClassifier
from ..iteration_data.domain_feature_data import DomainFeatureData
from ..iteration_data.instance_feature_data import InstanceFeatureData
from ..iteration_data.state_pair_equivalence import RuleEquivalences, StatePairEquivalence
from ..iteration_data.tuple_graph_equivalence import TupleGraphEquivalence

from .facts.instance_data.tuple_graph import TupleGraphFactFactory


class SketchASPFactory(ASPFactory):
    def __init__(self, config):
        super().__init__(config)
        self.ctl.add("equivalence_contains", ["i","s1", "s2", "r"], "equivalence_contains(i,s1,s2,r).")
        self.ctl.add("exceed", ["i", "s"], "exceed(i,s).")
        self.ctl.add("tuple", ["i", "s", "t"], "tuple(i,s,t).")
        self.ctl.add("contain", ["i", "s", "t", "r"], "contain(i,s,t,r).")
        self.ctl.add("t_distance", ["i", "s", "t", "d"], "t_distance(i,s,t,d).")
        self.ctl.add("d_distance", ["i", "s", "r", "d"], "d_distance(i,s,r,d).")
        self.ctl.add("r_distance", ["i", "s", "r", "d"], "r_distance(i,s,r,d).")
        self.ctl.load(str(config.asp_sketch_location))

    def make_facts(self, domain_feature_data: DomainFeatureData, rule_equivalences: RuleEquivalences, instance_datas: List[InstanceData], tuple_graphs_by_instance: List[List[TupleGraph]], tuple_graph_equivalences_by_instance: List[List[TupleGraphEquivalence]], state_pair_equivalences_by_instance: List[StatePairEquivalence], state_pair_classifiers_by_instance: List[StatePairClassifier], instance_feature_datas_by_instance: List[InstanceFeatureData]):
        """ Make facts from data in an interation. """
        facts = super().make_facts(domain_feature_data, rule_equivalences, instance_datas, tuple_graphs_by_instance, tuple_graph_equivalences_by_instance, state_pair_equivalences_by_instance, state_pair_classifiers_by_instance, instance_feature_datas_by_instance)
        for instance_data, tuple_graphs, tuple_graph_equivalences, state_pair_equivalence in zip(instance_datas, tuple_graphs_by_instance, tuple_graph_equivalences_by_instance, state_pair_equivalences_by_instance):
            for root_idx in tuple_graphs.keys():
                facts.extend(TupleGraphFactFactory().make_facts(instance_data.id, tuple_graphs[root_idx], state_pair_equivalence, tuple_graph_equivalences[root_idx]))
        return facts
