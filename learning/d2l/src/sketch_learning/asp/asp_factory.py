import re

from clingo import Control, Number, Symbol

from collections import defaultdict
from typing import List

from .returncodes import ClingoExitCode

from ..instance_data.state_pair import StatePair
from ..instance_data.instance_data import InstanceData
from ..iteration_data.domain_feature_data import DomainFeatureData
from ..iteration_data.state_pair_equivalence import DomainStatePairEquivalence


class ASPFactory:
    def __init__(self, config):
        self.ctl = Control(arguments=config.clingo_arguments + ["--opt-mode=optN"])
        # features
        self.ctl.add("boolean", ["b"], "boolean(b).")
        self.ctl.add("numerical", ["n"], "numerical(n).")
        self.ctl.add("feature", ["f"], "feature(f).")
        self.ctl.add("complexity", ["f", "c"], "complexity(f,c).")
        self.ctl.add("value", ["i","s","f","v"], "value(i,s,f,v).")
        # state space
        self.ctl.add("state", ["i", "s"], "state(i,s).")
        self.ctl.add("initial", ["i", "s"], "initial(i,s).")
        self.ctl.add("solvable", ["i", "s"], "solvable(i,s).")
        self.ctl.add("goal", ["i", "s"], "goal(i,s).")
        self.ctl.add("nongoal", ["i", "s"], "nongoal(i,s).")
        self.ctl.add("alive", ["i", "s"], "alive(i,s).")
        self.ctl.add("expanded", ["i", "s"], "expanded(i,s).")
        # rule equivalences
        self.ctl.add("feature_condition", ["f", "r", "v"], "feature_condition(f,r,v).")
        self.ctl.add("feature_effect", ["f", "r", "v"], "feature_effect(f,r,v).")
        self.ctl.add("state_pair_class", ["r"], "state_pair_class(r).")
        self.ctl.add("bad_state_pair_class", ["r"], "bad_state_pair_class(r).")
        # d2-separation constraints
        self.ctl.add("d2_separate", ["r1", "r2"], "d2_separate(r1,r2).")
        # tuple graph
        self.ctl.add("tuple", ["i", "s", "t"], "tuple(i,s,t).")
        self.ctl.add("contain", ["i", "s", "t", "r"], "contain(i,s,t,r).")
        self.ctl.add("cover", ["i", "s1", "s2", "r"], "cover(i,s1,s2,r).")
        self.ctl.add("t_distance", ["i", "s", "t", "d"], "t_distance(i,s,t,d).")
        self.ctl.add("d_distance", ["i", "s", "r", "d"], "d_distance(i,s,r,d).")
        self.ctl.add("r_distance", ["i", "s", "r", "d"], "r_distance(i,s,r,d).")
        self.ctl.load(str(config.asp_location))


    def make_facts(self, domain_feature_data: DomainFeatureData, domain_state_pair_equivalence: DomainStatePairEquivalence, instance_datas: List[InstanceData]):
        facts = []
        # State space facts
        for instance_data in instance_datas:
            instance_idx = instance_data.id
            for s_idx in instance_data.initial_s_idxs:
                facts.append(("initial", [Number(instance_idx), Number(s_idx)]))
            for s_idx in instance_data.state_space.get_state_indices():
                facts.append(("state", [Number(instance_idx), Number(s_idx)]))
                if not instance_data.goal_distance_information.is_deadend(s_idx):
                    facts.append(("solvable", [Number(instance_idx), Number(s_idx)]))
                if instance_data.goal_distance_information.is_goal(s_idx):
                    facts.append(("goal", [Number(instance_idx), Number(s_idx)]))
                else:
                    facts.append(("nongoal", [Number(instance_idx), Number(s_idx)]))
                if instance_data.goal_distance_information.is_alive(s_idx):
                    facts.append(("alive", [Number(instance_idx), Number(s_idx)]))
        # Domain feature facts
        for f_idx, boolean in enumerate(domain_feature_data.boolean_features):
            facts.append(("boolean", [Number(f_idx)]))
            facts.append(("feature", [Number(f_idx)]))
            facts.append(("complexity", [Number(f_idx), Number(boolean.compute_complexity())]))
        for f_idx, numerical in enumerate(domain_feature_data.numerical_features):
            facts.append(("numerical", [Number(f_idx + len(domain_feature_data.boolean_features))]))
            facts.append(("feature", [Number(f_idx + len(domain_feature_data.boolean_features))]))
            facts.append(("complexity", [Number(f_idx + len(domain_feature_data.boolean_features)), Number(numerical.compute_complexity())]))
        # Instance feature valuation facts
        for instance_data in instance_datas:
            for s_idx in instance_data.state_space.get_state_indices():
                feature_valuation = instance_data.feature_valuations[s_idx]
                for f_idx, f_val in enumerate(feature_valuation.boolean_feature_valuations):
                    facts.append(("value", [Number(instance_data.id), Number(s_idx), Number(f_idx), Number(f_val)]))
                for f_idx, f_val in enumerate(feature_valuation.numerical_feature_valuations):
                    facts.append(("value", [Number(instance_data.id), Number(s_idx), Number(f_idx + len(feature_valuation.boolean_feature_valuations)), Number(f_val)]))
        # State pair facts
        for r_idx, rule in enumerate(domain_state_pair_equivalence.rules):
            facts.append(("state_pair_class", [Number(r_idx)]))
            for condition in rule.get_conditions():
                condition_str = condition.str()
                result = re.findall(r"\(.* (\d+)\)", condition_str)
                assert len(result) == 1
                f_idx = int(result[0])
                if condition_str.startswith("(:c_b_pos"):
                    facts.append(("feature_condition", [Number(f_idx), Number(r_idx), Number(0)]))
                elif condition_str.startswith("(:c_b_neg"):
                    facts.append(("feature_condition", [Number(f_idx), Number(r_idx), Number(1)]))
                elif condition_str.startswith("(:c_n_gt"):
                    facts.append(("feature_condition", [Number(f_idx + len(domain_feature_data.boolean_features)), Number(r_idx), Number(2)]))
                elif condition_str.startswith("(:c_n_eq"):
                    facts.append(("feature_condition", [Number(f_idx + len(domain_feature_data.boolean_features)), Number(r_idx), Number(3)]))
                else:
                    raise Exception(f"Cannot parse condition {condition_str}")
            for effect in rule.get_effects():
                effect_str = effect.str()
                result = re.findall(r"\(.* (\d+)\)", effect_str)
                assert len(result) == 1
                f_idx = int(result[0])
                if effect_str.startswith("(:e_b_pos"):
                    facts.append(("feature_effect", [Number(f_idx), Number(r_idx), Number(0)]))
                elif effect_str.startswith("(:e_b_neg"):
                    facts.append(("feature_effect", [Number(f_idx), Number(r_idx), Number(1)]))
                elif effect_str.startswith("(:e_b_bot"):
                    facts.append(("feature_effect", [Number(f_idx), Number(r_idx), Number(2)]))
                elif effect_str.startswith("(:e_n_inc"):
                    facts.append(("feature_effect", [Number(f_idx + len(domain_feature_data.boolean_features)), Number(r_idx), Number(3)]))
                elif effect_str.startswith("(:e_n_dec"):
                    facts.append(("feature_effect", [Number(f_idx + len(domain_feature_data.boolean_features)), Number(r_idx), Number(4)]))
                elif effect_str.startswith("(:e_n_bot"):
                    facts.append(("feature_effect", [Number(f_idx + len(domain_feature_data.boolean_features)), Number(r_idx), Number(5)]))
                else:
                    raise Exception(f"Cannot parse effect {effect_str}")
        # State pair equivalence facts
        for instance_data in instance_datas:
            for state_pair, r_idx in instance_data.state_pair_equivalence.state_pair_to_r_idx.items():
                facts.append(("cover", [Number(instance_data.id), Number(state_pair.source_idx), Number(state_pair.target_idx), Number(r_idx)]))
        # Tuple graph equivalence facts
        for instance_data in instance_datas:
            for s_idx, tuple_graph_equivalence in instance_data.tuple_graph_equivalences.items():
                if not instance_data.goal_distance_information.is_alive(s_idx):
                    continue
                for t_idx, r_idxs in tuple_graph_equivalence.t_idx_to_r_idxs.items():
                    facts.append(("tuple", [Number(instance_data.id), Number(s_idx), Number(t_idx)]))
                    for r_idx in r_idxs:
                        facts.append(("contain", [Number(instance_data.id), Number(s_idx), Number(t_idx), Number(r_idx)]))
                for t_idx, d in tuple_graph_equivalence.t_idx_to_distance.items():
                    facts.append(("t_distance", [Number(instance_data.id), Number(s_idx), Number(t_idx), Number(d)]))
                for r_idx, d in tuple_graph_equivalence.r_idx_to_deadend_distance.items():
                    facts.append(("d_distance", [Number(instance_data.id), Number(s_idx), Number(r_idx), Number(d)]))
                for r_idx, d in tuple_graph_equivalence.r_idx_to_distance.items():
                    facts.append(("r_distance", [Number(instance_data.id), Number(s_idx), Number(r_idx), Number(d)]))
        return facts

    def make_initial_d2_facts(self, instance_datas: List[InstanceData]):
        """ T_0 facts """
        facts = set()
        for instance_data in instance_datas:
            for s_idx, tuple_graph in instance_data.tuple_graphs.items():
                equivalences = set()
                for s_prime_idxs in tuple_graph.get_state_indices_by_distance():
                    for s_prime_idx in s_prime_idxs:
                        equivalences.add(instance_data.state_pair_equivalence.state_pair_to_r_idx[StatePair(s_idx, s_prime_idx)])
                for i, eq_1 in enumerate(equivalences):
                    for j, eq_2 in enumerate(equivalences):
                        if i < j:
                            facts.add(("d2_separate", (Number(eq_1), Number(eq_2))))
        return facts

    def make_unsatisfied_d2_facts(self, symbols: List[Symbol], rule_equivalences: DomainStatePairEquivalence):
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
            for model in solve_handle:
                if model.optimality_proven:
                    return model.symbols(shown=True), ClingoExitCode.SATISFIABLE
            if solve_handle.get().unsatisfiable:
                return None, ClingoExitCode.UNSATISFIABLE
            return None, ClingoExitCode.UNKNOWN

    def print_statistics(self):
        print("Clingo statistics:")
        print("Total time: ", self.ctl.statistics["summary"]["times"]["total"])
        print("CPU time: ", self.ctl.statistics["summary"]["times"]["cpu"])
        print("Solve time: ", self.ctl.statistics["summary"]["times"]["solve"])
