from clingo import Control

from typing import List, Dict, Tuple

from ..instance_data.subproblem import Subproblem
from ..instance_data.instance_data import InstanceData
from ..instance_data.state_pair_classifier import StatePairClassifier
from ..iteration_data.domain_feature_data import DomainFeatureData
from ..iteration_data.instance_feature_data import InstanceFeatureData
from ..iteration_data.state_pair_equivalence import RuleEquivalences, StatePairEquivalence

from .facts.instance_data.transition_system import TransitionSystemFactFactory
from .facts.instance_data.state_pair_classifier import StatePairClassifierFactFactory
from .facts.iteration_data.domain_feature_data import DomainFeatureDataFactFactory
from .facts.iteration_data.equivalence_data import EquivalenceDataFactFactory
from .facts.iteration_data.instance_feature_data import InstanceFeatureDataFactFactory

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
        self.ctl.add("change", ["f", "r", "v"], "change(f,r,v).")

        self.ctl.add("expanded", ["i", "s"], "expanded(i,s).")  # basically alive states
        self.ctl.add("optimal_equivalence", ["i", "c", "s1", "s2"], "optimal_equivalence(i,c,s1,s2).")
        self.ctl.add("suboptimal_equivalence", ["i", "c", "s1", "s2"], "suboptimal_equivalence(i,c,s1,s2).")
        self.ctl.load(str(config.asp_policy_location))

    def make_facts(self, domain_feature_data: DomainFeatureData, rule_equivalences: RuleEquivalences, instance_datas: List[InstanceData], state_pair_equivalences_by_instance: List[StatePairEquivalence], state_pair_classifiers_by_instance: List[StatePairClassifier], instance_feature_datas_by_instance: List[InstanceFeatureData]):
        facts = []
        facts.extend(DomainFeatureDataFactFactory().make_facts(domain_feature_data))
        facts.extend(EquivalenceDataFactFactory().make_facts(rule_equivalences, domain_feature_data))
        for state_pair_equivalence, instance_data, state_pair_classifier, instance_feature_data in zip(state_pair_equivalences_by_instance, instance_datas, state_pair_classifiers_by_instance, instance_feature_datas_by_instance):
            facts.extend(TransitionSystemFactFactory().make_facts(instance_data.id, instance_data.transition_system, state_pair_classifier))
            facts.extend(InstanceFeatureDataFactFactory().make_facts(instance_data.id, instance_feature_data, state_pair_classifier))
            facts.extend(StatePairClassifierFactFactory().make_facts(instance_data.id, state_pair_classifier, state_pair_equivalence))
            pass
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
