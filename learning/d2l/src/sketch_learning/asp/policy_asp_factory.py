from clingo import Control, Symbol, String, Number, TruthValue, HeuristicType, Model, SolveResult

from typing import List, Dict, Tuple

from ..instance_data.instance_data import InstanceData
from ..instance_data.general_subproblem import GeneralSubproblemData
from ..iteration_data.feature_data import DomainFeatureData, InstanceFeatureData
from ..iteration_data.state_pair_equivalence_data import RuleEquivalenceData, StatePairEquivalenceData
from ..iteration_data.tuple_graph_equivalence_data import TupleGraphEquivalenceData

from .facts.iteration_data.domain_feature_data import DomainFeatureDataFactFactory
from .facts.iteration_data.equivalence_data import EquivalenceDataFactFactory
from .facts.instance_data.tuple_graph import TupleGraphFactFactory
from .facts.instance_data.general_subproblem import GeneralSubproblemDataFactFactory

class PolicyASPFactory:
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

        self.ctl.add("expanded", ["i", "g", "s"], "expanded(i,g,s).")
        self.ctl.add("subproblem", ["i", "s", "g"], "subproblem(i,s,g).")
        self.ctl.add("optimal_equivalence", ["i", "g", "c", "s1", "s2"], "optimal_equivalence(i,g,c,s1,s2).")
        self.ctl.add("suboptimal_equivalence", ["i", "g", "c", "s1", "s2"], "suboptimal_equivalence(i,g,c,s1,s2).")
        self.ctl.load(str(config.asp_policy_location))

    def make_facts(self, instance_datas: List[InstanceData], domain_feature_data: DomainFeatureData, rule_equivalence_data: RuleEquivalenceData, state_pair_equivalence_datas: List[StatePairEquivalenceData], general_subproblem_datas: List[GeneralSubproblemData]):
        facts = []
        facts.extend(DomainFeatureDataFactFactory().make_facts(domain_feature_data))
        facts.extend(EquivalenceDataFactFactory().make_facts(rule_equivalence_data, domain_feature_data))
        for instance_idx, (instance_data, state_pair_equivalence_data, general_subproblem_data) in enumerate(zip(instance_datas, state_pair_equivalence_datas, general_subproblem_datas)):
            facts.extend(GeneralSubproblemDataFactFactory().make_facts(instance_idx, state_pair_equivalence_data, general_subproblem_data))
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
