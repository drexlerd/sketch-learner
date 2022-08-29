from clingo import Control, Number, Symbol

from collections import defaultdict
from typing import List

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


class SketchASPFactory:
    def __init__(self, config):
        self.ctl = Control(arguments=["-c", f"max_sketch_rules={config.max_sketch_rules}"] + config.clingo_arguments)
        self.ctl.add("boolean", ["b"], "boolean(b).")
        self.ctl.add("numerical", ["n"], "numerical(n).")
        self.ctl.add("feature", ["f"], "feature(f).")
        self.ctl.add("complexity", ["f", "c"], "complexity(f, c).")
        self.ctl.add("value", ["i","s","f","v"], "value(i,s,f,v).")
        self.ctl.add("c_b_pos", ["r", "f"], "c_b_pos(r,f).")
        self.ctl.add("c_b_neg", ["r", "f"], "c_b_neg(r,f).")
        self.ctl.add("c_n_gt", ["r", "f"], "c_n_gt(r,f).")
        self.ctl.add("c_n_eq", ["r", "f"], "c_n_eq(r,f).")
        self.ctl.add("e_b_pos", ["r", "f"], "e_b_pos(r,f).")
        self.ctl.add("e_b_neg", ["r", "f"], "e_b_neg(r,f).")
        self.ctl.add("e_b_bot", ["r", "f"], "e_b_bot(r,f).")
        self.ctl.add("e_n_inc", ["r", "f"], "e_n_inc(r,f).")
        self.ctl.add("e_n_dec", ["r", "f"], "e_n_dec(r,f).")
        self.ctl.add("e_n_bot", ["r", "f"], "e_n_bot(r,f).")
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
        self.ctl.add("d2_separate", ["r1", "r2"], "d2_separate(r1,r2).")
        self.ctl.load(str(config.asp_sketch_location))

    def make_facts(self, domain_feature_data: DomainFeatureData, rule_equivalence_data: RuleEquivalences, instance_datas: List[InstanceData], tuple_graphs_by_instance: List[List[TupleGraph]], tuple_graph_equivalences_by_instance: List[List[TupleGraphEquivalence]], state_pair_equivalences_by_instance: List[StatePairEquivalence], state_pair_classifiers_by_instance: List[StatePairClassifier], instance_feature_datas: List[InstanceFeatureData]):
        """ Make facts from data in an interation. """
        facts = []
        facts.extend(DomainFeatureDataFactFactory().make_facts(domain_feature_data))
        facts.extend(EquivalenceDataFactFactory().make_facts(rule_equivalence_data, domain_feature_data))
        for instance_idx, (instance_data, tuple_graphs, tuple_graph_equivalences, state_pair_equivalence, state_pair_classifier, instance_feature_data) in enumerate(zip(instance_datas, tuple_graphs_by_instance, tuple_graph_equivalences_by_instance, state_pair_equivalences_by_instance, state_pair_classifiers_by_instance, instance_feature_datas)):
            facts.extend(TransitionSystemFactFactory().make_facts(instance_idx, instance_data.transition_system, state_pair_classifier))
            facts.extend(StatePairClassifierFactFactory().make_facts(instance_idx, state_pair_classifier, state_pair_equivalence))
            facts.extend(InstanceFeatureDataFactFactory().make_facts(instance_idx, instance_feature_data, state_pair_classifier))
            for tuple_graph, tuple_graph_equivalences in zip(tuple_graphs, tuple_graph_equivalences):
                facts.extend(TupleGraphFactFactory().make_facts(instance_idx, tuple_graph, state_pair_equivalence, tuple_graph_equivalences))
                pass
        return facts

    def make_initial_d2_facts(self, state_pair_classifiers_by_instance: List[StatePairClassifier], state_pair_equivalences_by_instance: List[StatePairEquivalence]):
        """ T_0 facts """
        facts = set()
        for state_pair_classifier, state_pair_equivalence in zip(state_pair_classifiers_by_instance, state_pair_equivalences_by_instance):
            for s_idx, state_pairs in state_pair_classifier.source_idx_to_state_pairs.items():
                equivalences = set()
                for state_pair in state_pairs:
                    equivalences.add(state_pair_equivalence.state_pair_to_r_idx[(state_pair.source_idx, state_pair.target_idx)])
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
        rule_to_feature_to_change = defaultdict(dict)
        for symbol in symbols:
            if symbol.name in {"e_b_pos", "e_b_neg", "e_b_bot", "e_n_inc", "e_n_dec", "e_n_bot"} and symbol.arguments[1].number in selected_feature_idxs:
                r_idx = symbol.arguments[0].number
                f_idx = symbol.arguments[1].number
                rule_to_feature_to_change[r_idx][f_idx] = symbol.name
        facts = set()
        for good in good_equivalences:
            for bad in bad_equivalences:
                # there must exist a selected feature that distinguishes them
                exists_distinguishing_feature = False
                for f_idx in selected_feature_idxs:
                    effect_good = rule_to_feature_to_change[good][f_idx]
                    effect_bad = rule_to_feature_to_change[bad][f_idx]
                    assert effect_good is not None and effect_bad is not None
                    if effect_good != effect_bad:
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
            return last_model.symbols(shown=True)

    def print_statistics(self):
        print("Clingo statistics:")
        print("Total time: ", self.ctl.statistics["summary"]["times"]["total"])
        print("CPU time: ", self.ctl.statistics["summary"]["times"]["cpu"])
        print("Solve time: ", self.ctl.statistics["summary"]["times"]["solve"])
