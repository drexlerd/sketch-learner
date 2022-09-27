from clingo import Number
from typing import List

from .asp_factory import ASPFactory

from ..instance_data.instance_data import InstanceData
from ..iteration_data.domain_feature_data import DomainFeatureData
from ..iteration_data.state_pair_equivalence import DomainStatePairEquivalence
from ..iteration_data.state_equivalence import DomainStateEquivalence


class SketchASPFactory(ASPFactory):
    def __init__(self, config):
        super().__init__(config)
        self.ctl.add("equivalence_contains", ["r", "d1", "d2"], "equivalence_contains(r,d1,d2).")
        self.ctl.add("exceed", ["i", "s"], "exceed(i,s).")
        self.ctl.add("tuple", ["i", "s", "t"], "tuple(i,s,t).")
        self.ctl.add("contain", ["i", "s", "t", "r"], "contain(i,s,t,r).")
        self.ctl.add("t_distance", ["i", "s", "t", "d"], "t_distance(i,s,t,d).")
        self.ctl.add("d_distance", ["i", "s", "r", "d"], "d_distance(i,s,r,d).")
        self.ctl.add("r_distance", ["i", "s", "r", "d"], "r_distance(i,s,r,d).")
        self.ctl.load(str(config.asp_sketch_location))

    def make_facts(self, domain_feature_data: DomainFeatureData, domain_state_equivalence: DomainStateEquivalence, rule_equivalences: DomainStatePairEquivalence, instance_datas: List[InstanceData]):
        """ Make facts from data in an interation. """
        facts = super().make_facts(domain_feature_data, domain_state_equivalence, rule_equivalences, instance_datas)
        for instance_data in instance_datas:
            for s_idx, tuple_graph in instance_data.tuple_graphs.items():
                tuple_graph = instance_data.tuple_graphs[s_idx]
                tuple_graph_equivalence = instance_data.tuple_graph_equivalences[s_idx]
                facts.append(("exceed", [Number(instance_data.id), Number(tuple_graph.root_idx)]))
                for d in range(len(tuple_graph.t_idxs_by_distance)):
                    for t_idx in tuple_graph.t_idxs_by_distance[d]:
                        facts.append(("t_distance", [Number(instance_data.id), Number(tuple_graph.root_idx), Number(t_idx), Number(d)]))
                        facts.append(("tuple", [Number(instance_data.id), Number(tuple_graph.root_idx), Number(t_idx)]))
                        for r_idx in tuple_graph_equivalence.t_idx_to_r_idxs[t_idx]:
                            facts.append(("contain", [Number(instance_data.id), Number(tuple_graph.root_idx), Number(t_idx), Number(r_idx)]))
                for r_idx, d in tuple_graph_equivalence.r_idx_to_deadend_distance.items():
                    facts.append(("d_distance", [Number(instance_data.id), Number(tuple_graph.root_idx), Number(r_idx), Number(d)]))
                for r_idx, d in tuple_graph_equivalence.r_idx_to_distance.items():
                    facts.append(("r_distance", [Number(instance_data.id), Number(tuple_graph.root_idx), Number(r_idx), Number(d)]))
                    if d == 0:
                        facts.append(("looping_equivalences", (Number(r_idx),)))
                for r_idx, state_class_pairs in instance_data.state_pair_equivalence.r_idx_to_state_class_pairs.items():
                    for state_class_pair in state_class_pairs:
                        facts.append(("equivalence_contains", [Number(r_idx), Number(state_class_pair[0]), Number(state_class_pair[1])]))
        return facts
