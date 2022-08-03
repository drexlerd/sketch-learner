from clingo import Control, Symbol, String, Number, TruthValue, HeuristicType, Model, SolveResult

from typing import List, Dict, Tuple

from ..instance_data.instance_data import InstanceData
from ..iteration_data.feature_data import DomainFeatureData, InstanceFeatureData
from ..iteration_data.state_pair_equivalence_data import RuleEquivalenceData, StatePairEquivalenceData
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

        self.ctl.add("equivalence_contains", ["i","s1", "s2", "r"], "equivalence_contains(i,s1,s2,r).")
        self.ctl.add("solvable", ["i", "s"], "solvable(i,s).")
        self.ctl.add("exceed", ["i", "s"], "exceed(i,s).")
        self.ctl.add("t_distance", ["i", "s", "t", "d"], "t_distance(i,s,t,d).")
        self.ctl.add("tuple", ["i", "s", "t"], "tuple(i,s,t).")
        self.ctl.add("contain", ["i", "s", "t", "r"], "contain(i,s,t,r).")
        self.ctl.add("d_distance", ["i", "s", "r", "d"], "d_distance(i,s,r,d).")
        self.ctl.add("consistency", ["i", "s1", "s2", "t"], "consistency(i,s1,s2,t).")
        self.ctl.load(str(config.asp_sketch_location))

    def make_facts(self, instance_datas: List[InstanceData], domain_feature_data: DomainFeatureData, rule_equivalence_data: RuleEquivalenceData, state_pair_equivalence_datas: List[StatePairEquivalenceData], tuple_graph_equivalence_datas: List[TupleGraphEquivalenceData]):
        """ Make facts from data in an interation. """
        facts = []
        facts.extend(DomainFeatureDataFactFactory().make_facts(domain_feature_data))
        facts.extend(EquivalenceDataFactFactory().make_facts(rule_equivalence_data, domain_feature_data))
        for instance_idx, (instance_data, state_pair_equivalence_data, tuple_graph_equivalence_data) in enumerate(zip(instance_datas, state_pair_equivalence_datas, tuple_graph_equivalence_datas)):
            facts.extend(TransitionSystemFactFactory().make_facts(instance_idx, instance_data.transition_system))
            for tuple_graph, tuple_graph_equivalence_data in zip(instance_data.tuple_graphs_by_state_index, tuple_graph_equivalence_data):
                facts.extend(TupleGraphFactFactory().make_facts(instance_idx, tuple_graph, state_pair_equivalence_data, tuple_graph_equivalence_data))
        return facts

    def ground(self, facts=[]):
        facts.append(("base", []))
        self.ctl.ground(facts)  # ground a set of facts

    def solve(self):
        with self.ctl.solve(yield_=True) as solve_handle:
            while not solve_handle.get().exhausted:
                model = solve_handle.model()
                solve_handle.resume()
            if solve_handle.get().exhausted: print("exhausted")
            if solve_handle.get().interrupted: print("interrupted")
            if solve_handle.get().satisfiable: print("satisfiable")
            if solve_handle.get().unknown: print("unknown")
            if solve_handle.get().unsatisfiable: print("unsatisfiable")
            return model

    def print_statistics(self):
        print("Clingo statistics:")
        print(self.ctl.statistics)
        print("Total time: ", self.ctl.statistics["summary"]["times"]["total"])
        print("CPU time: ", self.ctl.statistics["summary"]["times"]["cpu"])
        print("Solve time: ", self.ctl.statistics["summary"]["times"]["solve"])
