from clingo import Control

from typing import List

from ..instance_data.instance_data import InstanceData
from ..instance_data.tuple_graph_data import TupleGraphData
from ..iteration_data.domain_feature_data import DomainFeatureData
from ..iteration_data.instance_feature_data import InstanceFeatureData
from ..iteration_data.state_pair_equivalence import RuleEquivalences, StatePairEquivalence
from ..iteration_data.tuple_graph_equivalence_data import TupleGraphEquivalenceData

from .facts.iteration_data.domain_feature_data import DomainFeatureDataFactFactory
from .facts.iteration_data.equivalence_data import EquivalenceDataFactFactory
from .facts.instance_data.tuple_graph import TupleGraphFactFactory
from .facts.instance_data.transition_system import TransitionSystemFactFactory


class SketchASPFactory:
    def __init__(self, config):
        self.ctl = Control(arguments=["-c", f"max_sketch_rules={config.max_sketch_rules}"] + config.clingo_arguments)
        self.ctl.add("boolean", ["b"], "boolean(b).")
        self.ctl.add("numerical", ["n"], "numerical(n).")
        self.ctl.add("feature", ["f"], "feature(f).")
        self.ctl.add("complexity", ["f", "c"], "complexity(f, c).")
        self.ctl.add("value", ["i","s","f","v"], "value(i,s,f,v).")
        self.ctl.add("c_pos_fixed", ["r", "f"], "c_pos_fixed(r,f).")
        self.ctl.add("c_neg_fixed", ["r", "f"], "c_neg_fixed(r,f).")
        self.ctl.add("c_gt_fixed", ["r", "f"], "c_gt_fixed(r,f).")
        self.ctl.add("c_eq_fixed", ["r", "f"], "c_eq_fixed(r,f).")
        self.ctl.add("e_pos_fixed", ["r", "f"], "e_pos_fixed(r,f).")
        self.ctl.add("e_neg_fixed", ["r", "f"], "e_neg_fixed(r,f).")
        self.ctl.add("e_bot_fixed", ["r", "f"], "e_bot_fixed(r,f).")
        self.ctl.add("e_inc_fixed", ["r", "f"], "e_inc_fixed(r,f).")
        self.ctl.add("e_dec_fixed", ["r", "f"], "e_dec_fixed(r,f).")
        self.ctl.add("e_bot_fixed", ["r", "f"], "e_bot_fixed(r,f).")
        self.ctl.add("equivalence", ["r"], "equivalence(r).")
        self.ctl.add("goal", ["i", "s"], "goal(i,s).")
        self.ctl.add("nongoal", ["i", "s"], "nongoal(i,s).")
        self.ctl.add("change", ["f", "r", "v"], "change(f,r,v).")

        self.ctl.add("equivalence_contains", ["i","s1", "s2", "r"], "equivalence_contains(i,s1,s2,r).")
        self.ctl.add("solvable", ["i", "s"], "solvable(i,s).")
        self.ctl.add("exceed", ["i", "s"], "exceed(i,s).")
        self.ctl.add("tuple", ["i", "s", "t"], "tuple(i,s,t).")
        self.ctl.add("contain", ["i", "s", "t", "r"], "contain(i,s,t,r).")
        self.ctl.add("t_distance", ["i", "s", "t", "d"], "t_distance(i,s,t,d).")
        self.ctl.add("d_distance", ["i", "s", "r", "d"], "d_distance(i,s,r,d).")
        self.ctl.add("r_distance", ["i", "s", "r", "d"], "r_distance(i,s,r,d).")
        self.ctl.load(str(config.asp_sketch_location))

    def make_facts(self, instance_datas: List[InstanceData], tuple_graph_datas: List[TupleGraphData], domain_feature_data: DomainFeatureData, rule_equivalence_data: RuleEquivalences, state_pair_equivalence_datas: List[StatePairEquivalence], tuple_graph_equivalence_datas: List[TupleGraphEquivalenceData], instance_feature_datas: List[InstanceFeatureData]):
        """ Make facts from data in an interation. """
        facts = []
        facts.extend(DomainFeatureDataFactFactory().make_facts(domain_feature_data))
        facts.extend(EquivalenceDataFactFactory().make_facts(rule_equivalence_data, domain_feature_data))
        for instance_idx, (instance_data, state_pair_equivalence_data, tuple_graph_data, tuple_graph_equivalence_data, instance_feature_data) in enumerate(zip(instance_datas, state_pair_equivalence_datas, tuple_graph_datas, tuple_graph_equivalence_datas, instance_feature_datas)):
            facts.extend(TransitionSystemFactFactory().make_facts(instance_idx, instance_data.transition_system, instance_feature_data))
            for tuple_graph, tuple_graph_equivalence_data in zip(tuple_graph_data.tuple_graphs_by_state_index, tuple_graph_equivalence_data.tuple_graph_equivalence_by_state_index):
                facts.extend(TupleGraphFactFactory().make_facts(instance_idx, tuple_graph, state_pair_equivalence_data, tuple_graph_equivalence_data))
        return facts

    def ground(self, facts=[]):
        facts.append(("base", []))
        self.ctl.ground(facts)  # ground a set of facts

    def solve(self):
        with self.ctl.solve(yield_=True) as solve_handle:
            last_model = None
            for model in solve_handle:
                last_model = model
                solve_result = solve_handle.get()
            return last_model.symbols(shown=True)

    def print_statistics(self):
        print("Clingo statistics:")
        print("Total time: ", self.ctl.statistics["summary"]["times"]["total"])
        print("CPU time: ", self.ctl.statistics["summary"]["times"]["cpu"])
        print("Solve time: ", self.ctl.statistics["summary"]["times"]["solve"])
