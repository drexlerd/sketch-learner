from clingo import Control, Number, Symbol

from collections import defaultdict
from typing import List

from .returncodes import ClingoExitCode

from ..instance_data.instance_data import InstanceData
from ..instance_data.tuple_graph import TupleGraph
from ..instance_data.state_pair_classifier import StatePairClassifier
from ..iteration_data.domain_feature_data import DomainFeatureData
from ..iteration_data.instance_feature_data import InstanceFeatureData
from ..iteration_data.state_pair_equivalence import RuleEquivalences, StatePairEquivalence
from ..iteration_data.tuple_graph_equivalence import TupleGraphEquivalence

from .facts.instance_data.tuple_graph import TupleGraphFactFactory
from .facts.instance_data.transition_system import TransitionSystemFactFactory
from .facts.instance_data.state_pair_classifier import StatePairClassifierFactFactory
from .facts.iteration_data.domain_feature_data import DomainFeatureDataFactFactory
from .facts.iteration_data.equivalence_data import EquivalenceDataFactFactory
from .facts.iteration_data.instance_feature_data import InstanceFeatureDataFactFactory


class ASPFactory:
    def __init__(self, config):
        self.ctl = Control(arguments=config.clingo_arguments)
        # features
        self.ctl.add("boolean", ["b"], "boolean(b).")
        self.ctl.add("numerical", ["n"], "numerical(n).")
        self.ctl.add("feature", ["f"], "feature(f).")
        self.ctl.add("complexity", ["f", "c"], "complexity(f,c).")
        self.ctl.add("value", ["i","s","f","v"], "value(i,s,f,v).")
        # transition system
        self.ctl.add("solvable", ["i", "s"], "solvable(i,s).")
        self.ctl.add("goal", ["i", "s"], "goal(i,s).")
        self.ctl.add("nongoal", ["i", "s"], "nongoal(i,s).")
        self.ctl.add("alive", ["i", "s"], "alive(i,s).")
        self.ctl.add("expanded", ["i", "s"], "expanded(i,s).")
        # rule equivalences
        self.ctl.add("feature_condition", ["f", "r", "v"], "feature_condition(f,r,v).")
        self.ctl.add("feature_effect", ["f", "r", "v"], "feature_effect(f,r,v).")
        self.ctl.add("equivalence", ["r"], "equivalence(r).")
        # d2-separation constraints
        self.ctl.add("d2_separate", ["r1", "r2"], "d2_separate(r1,r2).")
        # optimality
        self.ctl.add("looping_equivalences", ["r"], "looping_equivalences(r).")  # we use delta optimal here instead
        self.ctl.add("delta_optimal", ["i", "c", "s1", "s2"], "delta_optimal(i,c,s1,s2).")
        self.ctl.add("not_delta_optimal", ["i", "c", "s1", "s2"], "not_delta_optimal(i,c,s1,s2).")

    def make_facts(self, domain_feature_data: DomainFeatureData, rule_equivalences: RuleEquivalences, instance_datas: List[InstanceData], tuple_graphs_by_instance: List[List[TupleGraph]], tuple_graph_equivalences_by_instance: List[List[TupleGraphEquivalence]], state_pair_equivalences_by_instance: List[StatePairEquivalence], state_pair_classifiers_by_instance: List[StatePairClassifier], instance_feature_datas_by_instance: List[InstanceFeatureData]):
        facts = []
        facts.extend(DomainFeatureDataFactFactory().make_facts(domain_feature_data))
        facts.extend(EquivalenceDataFactFactory().make_facts(rule_equivalences, domain_feature_data))
        for state_pair_equivalence, instance_data, state_pair_classifier, instance_feature_data in zip(state_pair_equivalences_by_instance, instance_datas, state_pair_classifiers_by_instance, instance_feature_datas_by_instance):
            facts.extend(TransitionSystemFactFactory().make_facts(instance_data.id, instance_data.transition_system, state_pair_classifier))
            facts.extend(InstanceFeatureDataFactFactory().make_facts(instance_data.id, instance_feature_data, state_pair_classifier))
            facts.extend(StatePairClassifierFactFactory().make_facts(instance_data.id, state_pair_classifier, state_pair_equivalence))
        return facts

    def make_initial_d2_facts(self, state_pair_classifiers_by_instance: List[StatePairClassifier], state_pair_equivalences_by_instance: List[StatePairEquivalence]):
        """ T_0 facts """
        facts = set()
        for state_pair_classifier, state_pair_equivalence in zip(state_pair_classifiers_by_instance, state_pair_equivalences_by_instance):
            for s_idx, state_pairs in state_pair_classifier.source_idx_to_state_pairs.items():
                equivalences = set()
                for state_pair in state_pairs:
                    equivalences.add(state_pair_equivalence.state_pair_to_r_idx[state_pair])
                for i, eq_1 in enumerate(equivalences):
                    for j, eq_2 in enumerate(equivalences):
                        if i < j:
                            facts.add(("d2_separate", (Number(eq_1), Number(eq_2))))
        return facts

    def make_unsatisfied_d2_facts(self, symbols: List[Symbol], rule_equivalences: RuleEquivalences):
        # compute good and bad equivalences
        good_equivalences = set()
        for symbol in symbols:
            if symbol.name == "good":
                good_equivalences.add(symbol.arguments[0].number)
        bad_equivalences = set([r_idx for r_idx in range(len(rule_equivalences.rules)) if r_idx not in good_equivalences])
        # compute selected features
        selected_feature_idxs = set()
        for symbol in symbols:
            if symbol.name == "select":
                selected_feature_idxs.add(symbol.arguments[0].number)
        # preprocess symbols
        rule_to_feature_to_condition = defaultdict(dict)
        rule_to_feature_to_effect = defaultdict(dict)
        for symbol in symbols:
            if symbol.name == "feature_condition":
                f_idx = symbol.arguments[0].number
                r_idx = symbol.arguments[1].number
                condition = symbol.arguments[2].number
                rule_to_feature_to_condition[r_idx][f_idx] = condition
            if symbol.name == "feature_effect":
                f_idx = symbol.arguments[0].number
                r_idx = symbol.arguments[1].number
                effect = symbol.arguments[2].number
                rule_to_feature_to_effect[r_idx][f_idx] = effect
        facts = set()
        for good in good_equivalences:
            for bad in bad_equivalences:
                # there must exist a selected feature that distinguishes them
                exists_distinguishing_feature = False
                for f_idx in selected_feature_idxs:
                    condition_good = rule_to_feature_to_condition[good][f_idx]
                    condition_bad = rule_to_feature_to_condition[bad][f_idx]
                    effect_good = rule_to_feature_to_effect[good][f_idx]
                    effect_bad = rule_to_feature_to_effect[bad][f_idx]
                    assert condition_good is not None and condition_bad is not None and \
                        effect_good is not None and effect_bad is not None
                    if condition_good != condition_bad or \
                        effect_good != effect_bad:
                        exists_distinguishing_feature = True
                        break
                if not exists_distinguishing_feature:
                    facts.add(("d2_separate", (Number(good), Number(bad))))
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
