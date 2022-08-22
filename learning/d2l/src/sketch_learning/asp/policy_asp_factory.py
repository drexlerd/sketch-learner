from clingo import Control, Symbol, String, Number, TruthValue, HeuristicType, Model, SolveResult

from typing import List, Dict, Tuple

from ..instance_data.instance_data import InstanceData
from ..instance_data.subproblem import SubproblemData
from ..iteration_data.domain_feature_data import DomainFeatureData
from ..iteration_data.instance_feature_data import InstanceFeatureData
from ..iteration_data.state_pair_equivalence_data import RuleEquivalenceData, StatePairEquivalenceData
from ..iteration_data.tuple_graph_equivalence_data import TupleGraphEquivalenceData

from .facts.iteration_data.domain_feature_data import DomainFeatureDataFactFactory
from .facts.iteration_data.equivalence_data import EquivalenceDataFactFactory
from .facts.instance_data.tuple_graph import TupleGraphFactFactory
from .facts.instance_data.general_subproblem import SubproblemDataFactFactory

from .returncodes import ClingoExitCode


class PolicyASPFactory:
    def __init__(self, config):
        self.ctl = Control(arguments=["-c", f"max_sketch_rules={config.max_sketch_rules}"] + config.clingo_arguments)
        self.ctl.add("boolean", ["b"], "boolean(b).")
        self.ctl.add("numerical", ["n"], "numerical(n).")
        self.ctl.add("feature", ["f"], "feature(f).")
        self.ctl.add("complexity", ["f", "c"], "complexity(f,c).")
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

        self.ctl.add("expanded", ["i", "s"], "expanded(i,s).")
        self.ctl.add("optimal_equivalence", ["i", "c", "s1", "s2"], "optimal_equivalence(i,c,s1,s2).")
        self.ctl.add("suboptimal_equivalence", ["i", "c", "s1", "s2"], "suboptimal_equivalence(i,c,s1,s2).")
        self.ctl.add("change", ["f", "r", "v"], "change(f,r,v).")
        self.ctl.load(str(config.asp_policy_location))

    def make_facts(self, domain_feature_data: DomainFeatureData, rule_equivalence_data: RuleEquivalenceData, state_pair_equivalence_datas: List[StatePairEquivalenceData], subproblem_datas: List[SubproblemData], instance_feature_datas: List[InstanceFeatureData]):
        facts = []
        facts.extend(DomainFeatureDataFactFactory().make_facts(domain_feature_data))
        facts.extend(EquivalenceDataFactFactory().make_facts(rule_equivalence_data, domain_feature_data))
        for state_pair_equivalence_data, general_subproblem_data, instance_feature_data in zip(state_pair_equivalence_datas, subproblem_datas, instance_feature_datas):
            facts.extend(SubproblemDataFactFactory().make_facts(state_pair_equivalence_data, general_subproblem_data, instance_feature_data))
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
            if solve_handle.get().unsatisfiable:
                return [], ClingoExitCode.UNSATISFIABLE
            else:
                return last_model.symbols(shown=True), ClingoExitCode.SATISFIABLE

    def print_statistics(self):
        print("Clingo statistics:")
        print("Total time: ", self.ctl.statistics["summary"]["times"]["total"])
        print("CPU time: ", self.ctl.statistics["summary"]["times"]["cpu"])
        print("Solve time: ", self.ctl.statistics["summary"]["times"]["solve"])
