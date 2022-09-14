from typing import List

from .asp_factory import ASPFactory

from ..instance_data.instance_data import InstanceData
from ..iteration_data.domain_feature_data import DomainFeatureData
from ..iteration_data.state_pair_equivalence import RuleEquivalences

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

    def make_facts(self, domain_feature_data: DomainFeatureData, rule_equivalences: RuleEquivalences, instance_datas: List[InstanceData]):
        """ Make facts from data in an interation. """
        facts = super().make_facts(domain_feature_data, rule_equivalences, instance_datas)
        for instance_data in instance_datas:
            for s_idx in instance_data.state_space.get_state_indices():
                facts.extend(TupleGraphFactFactory().make_facts(instance_data, s_idx))
        return facts
