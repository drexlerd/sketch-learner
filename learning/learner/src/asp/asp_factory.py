import re

from dlplan.core import Boolean, Numerical
from dlplan.policy import PositiveBooleanCondition, NegativeBooleanCondition, GreaterNumericalCondition, EqualNumericalCondition, PositiveBooleanEffect, NegativeBooleanEffect, UnchangedBooleanEffect, DecrementNumericalEffect, IncrementNumericalEffect, UnchangedNumericalEffect

from clingo import Control, Number, Symbol, String
from collections import defaultdict
from typing import List

from .returncodes import ClingoExitCode
from ..domain_data.domain_data import DomainData
from ..instance_data.instance_data import InstanceData


class ASPFactory:
    def __init__(self):
        self.ctl = Control(arguments=["--parallel-mode=32,split", "--opt-mode=optN"])
        # features
        self.ctl.add("boolean", ["b"], "boolean(b).")
        self.ctl.add("numerical", ["n"], "numerical(n).")
        self.ctl.add("feature", ["f"], "feature(f).")
        self.ctl.add("complexity", ["f", "c"], "complexity(f,c).")
        self.ctl.add("value", ["i","s","f","v"], "value(i,s,f,v).")
        self.ctl.add("b_value", ["i","s","f","v"], "b_value(i,s,f,v).")
        # state space
        self.ctl.add("state", ["i", "s"], "state(i,s).")
        self.ctl.add("initial", ["i", "s"], "initial(i,s).")
        self.ctl.add("solvable", ["i", "s"], "solvable(i,s).")
        self.ctl.add("unsolvable", ["i", "s"], "unsolvable(i,s).")
        self.ctl.add("goal", ["i", "s"], "goal(i,s).")
        self.ctl.add("nongoal", ["i", "s"], "nongoal(i,s).")
        self.ctl.add("alive", ["i", "s"], "alive(i,s).")
        self.ctl.add("expanded", ["i", "s"], "expanded(i,s).")
        # rule equivalences
        self.ctl.add("feature_condition", ["r", "f", "v"], "feature_condition(r,f,v).")
        self.ctl.add("feature_effect", ["r", "f", "v"], "feature_effect(r,f,v).")
        self.ctl.add("state_pair_class", ["r"], "state_pair_class(r).")
        # d2-separation constraints
        self.ctl.add("d2_separate", ["r1", "r2"], "d2_separate(r1,r2).")
        # tuple graph
        self.ctl.add("tuple", ["i", "s", "t"], "tuple(i,s,t).")
        self.ctl.add("contain", ["i", "s", "t", "r"], "contain(i,s,t,r).")
        self.ctl.add("cover", ["i", "s1", "s2", "r"], "cover(i,s1,s2,r).")
        self.ctl.add("t_distance", ["i", "s", "t", "d"], "t_distance(i,s,t,d).")
        self.ctl.add("d_distance", ["i", "s", "r", "d"], "d_distance(i,s,r,d).")
        self.ctl.add("r_distance", ["i", "s", "r", "d"], "r_distance(i,s,r,d).")
        self.ctl.add("s_distance", ["i", "s1", "s2", "d"], "s_distance(i,s1,s2,d).")

    def load_problem_file(self, filename):
        self.ctl.load(str(filename))

    def _create_initial_fact(self, instance_id: int, state_id: int):
        return ("initial", [Number(instance_id), Number(state_id)])

    def _create_state_fact(self, instance_id: int, state_id: int):
        return ("state", [Number(instance_id), Number(state_id)])

    def _create_solvable_fact(self, instance_id: int, state_id: int):
        return ("solvable", [Number(instance_id), Number(state_id)])

    def _create_unsolvable_fact(self, instance_id: int, state_id: int):
        return ("unsolvable", [Number(instance_id), Number(state_id)])

    def _create_goal_fact(self, instance_id: int, state_id: int):
        return ("goal", [Number(instance_id), Number(state_id)])

    def _create_nongoal_fact(self, instance_id: int, state_id: int):
        return ("nongoal", [Number(instance_id), Number(state_id)])

    def _create_alive_fact(self, instance_id: int, state_id: int):
        return ("alive", [Number(instance_id), Number(state_id)])

    def make_state_space_facts(self, instance_datas: List[InstanceData]):
        """ Create facts that encode the state space.
        """
        facts = []
        for instance_data in instance_datas:
            for s_idx in instance_data.initial_s_idxs:
                facts.append(self._create_initial_fact(instance_data.id, s_idx))
            for s_idx in instance_data.state_space.get_states().keys():
                facts.append(self._create_state_fact(instance_data.id, s_idx))
                if not instance_data.is_deadend(s_idx):
                    facts.append(self._create_solvable_fact(instance_data.id, s_idx))
                else:
                    facts.append(self._create_unsolvable_fact(instance_data.id, s_idx))
                if instance_data.is_goal(s_idx):
                    facts.append(self._create_goal_fact(instance_data.id, s_idx))
                else:
                    facts.append(self._create_nongoal_fact(instance_data.id, s_idx))
                if instance_data.is_alive(s_idx):
                    facts.append(self._create_alive_fact(instance_data.id, s_idx))
        return facts

    def _create_feature_fact(self, f_idx: int):
        return ("feature", [Number(f_idx)])

    def _create_complexity_fact(self, f_idx: int, complexity: int):
        return ("complexity", [Number(f_idx), Number(complexity)])

    def _create_boolean_fact(self, f_idx: int):
        return ("boolean", [Number(f_idx)])

    def _create_numerical_fact(self, f_idx: int):
        return ("numerical", [Number(f_idx)])

    def make_domain_feature_data_facts(self, domain_data: DomainData):
        facts = []
        # Domain feature facts
        for f_idx, feature in enumerate(domain_data.feature_pool.features):
            facts.append(self._create_feature_fact(f_idx))
            facts.append(self._create_complexity_fact(f_idx, feature.complexity))
            if isinstance(feature.dlplan_feature, Boolean):
                facts.append(self._create_boolean_fact(f_idx))
            elif isinstance(feature.dlplan_feature, Numerical):
                facts.append(self._create_numerical_fact(f_idx))
        return facts

    def make_instance_feature_data_facts(self, domain_data: DomainData, instance_datas: List[InstanceData]):
        facts = []
        # Instance feature valuation facts
        feature_pool = domain_data.feature_pool
        for instance_data in instance_datas:
            for s_idx in instance_data.state_space.get_states().keys():
                feature_valuation = instance_data.per_state_feature_valuations.s_idx_to_feature_valuations[s_idx]
                for f_idx, (feature, val) in enumerate(zip(feature_pool.features, feature_valuation.feature_valuations)):
                    facts.append(("value", [Number(instance_data.id), Number(s_idx), Number(f_idx), Number(val)]))
                    if isinstance(feature.dlplan_feature, Boolean):
                        facts.append(("b_value", [Number(instance_data.id), Number(s_idx), Number(f_idx), Number(val)]))
                    elif isinstance(feature.dlplan_feature, Numerical):
                        facts.append(("b_value", [Number(instance_data.id), Number(s_idx), Number(f_idx), Number(1 if val > 0 else 0)]))
        return facts

    def make_state_pair_equivalence_data_facts(self, domain_data: DomainData, instance_datas: List[InstanceData]):
        facts = []
        # State pair facts
        for r_idx, rule in enumerate(domain_data.domain_state_pair_equivalence.rules):
            facts.append(("state_pair_class", [Number(r_idx)]))
            for condition in rule.get_conditions():
                f_idx = int(condition.get_named_element().get_key())
                if isinstance(condition, PositiveBooleanCondition):
                    facts.append(("feature_condition", [Number(r_idx), Number(f_idx), Number(0)]))
                    facts.append(("c_pos_rule", [Number(r_idx), Number(f_idx)]))
                elif isinstance(condition, NegativeBooleanCondition):
                    facts.append(("feature_condition", [Number(r_idx), Number(f_idx), Number(1)]))
                    facts.append(("c_neg_rule", [Number(r_idx), Number(f_idx)]))
                elif isinstance(condition, GreaterNumericalCondition):
                    facts.append(("feature_condition", [Number(r_idx), Number(f_idx), Number(2)]))
                    facts.append(("c_gt_rule", [Number(r_idx), Number(f_idx)]))
                elif isinstance(condition, EqualNumericalCondition):
                    facts.append(("feature_condition", [Number(r_idx), Number(f_idx), Number(3)]))
                    facts.append(("c_eq_rule", [Number(r_idx), Number(f_idx)]))
                else:
                    raise RuntimeError(f"Cannot parse condition {str(condition)}")
            for effect in rule.get_effects():
                f_idx = int(effect.get_named_element().get_key())
                if isinstance(effect, PositiveBooleanEffect):
                    facts.append(("feature_effect", [Number(r_idx), Number(f_idx), Number(0)]))
                    facts.append(("e_pos_rule", [Number(r_idx), Number(f_idx)]))
                elif isinstance(effect, NegativeBooleanEffect):
                    facts.append(("feature_effect", [Number(r_idx), Number(f_idx), Number(1)]))
                    facts.append(("e_neg_rule", [Number(r_idx), Number(f_idx)]))
                elif isinstance(effect, UnchangedBooleanEffect):
                    facts.append(("feature_effect", [Number(r_idx), Number(f_idx), Number(2)]))
                    facts.append(("e_bot_rule", [Number(r_idx), Number(f_idx)]))
                elif isinstance(effect, IncrementNumericalEffect):
                    facts.append(("feature_effect", [Number(r_idx), Number(f_idx), Number(3)]))
                    facts.append(("e_inc_rule", [Number(r_idx), Number(f_idx)]))
                elif isinstance(effect, DecrementNumericalEffect):
                    facts.append(("feature_effect", [Number(r_idx), Number(f_idx), Number(4)]))
                    facts.append(("e_dec_rule", [Number(r_idx), Number(f_idx)]))
                elif isinstance(effect, UnchangedNumericalEffect):
                    facts.append(("feature_effect", [Number(r_idx), Number(f_idx), Number(5)]))
                    facts.append(("e_bot_rule", [Number(r_idx), Number(f_idx)]))
                else:
                    raise RuntimeError(f"Cannot parse effect {str(effect)}")
        # State pair equivalence facts
        for instance_data in instance_datas:
            for s_idx, state_pair_equivalence in instance_data.per_state_state_pair_equivalences.s_idx_to_state_pair_equivalence.items():
                if instance_data.is_deadend(s_idx):
                    continue
                for r_idx, d in state_pair_equivalence.r_idx_to_distance.items():
                    facts.append(("r_distance", [Number(instance_data.id), Number(s_idx), Number(r_idx), Number(d)]))
                for r_idx, s_prime_idxs in state_pair_equivalence.r_idx_to_subgoal_states.items():
                    for s_prime_idx in s_prime_idxs:
                        facts.append(("cover", [Number(instance_data.id), Number(s_idx), Number(s_prime_idx), Number(r_idx)]))
        return facts


    def make_tuple_graph_equivalence_facts(self, domain_data: DomainData, instance_datas: List[InstanceData]):
        facts = []
        # Tuple graph equivalence facts (Perhaps deprecated since we now let rules imply subgoals)
        for instance_data in instance_datas:
            for s_idx, tuple_graph_equivalence in instance_data.per_state_tuple_graph_equivalences.s_idx_to_tuple_graph_equivalence.items():
                if instance_data.is_deadend(s_idx):
                    continue
                for t_idx, r_idxs in tuple_graph_equivalence.t_idx_to_r_idxs.items():
                    facts.append(("tuple", [Number(instance_data.id), Number(s_idx), Number(t_idx)]))
                    for r_idx in r_idxs:
                        facts.append(("contain", [Number(instance_data.id), Number(s_idx), Number(t_idx), Number(r_idx)]))
                for t_idx, d in tuple_graph_equivalence.t_idx_to_distance.items():
                    facts.append(("t_distance", [Number(instance_data.id), Number(s_idx), Number(t_idx), Number(d)]))
                for r_idx, d in tuple_graph_equivalence.r_idx_to_deadend_distance.items():
                    facts.append(("d_distance", [Number(instance_data.id), Number(s_idx), Number(r_idx), Number(d)]))
        return facts

    def make_tuple_graph_facts(self, domain_data: DomainData, instance_datas: List[InstanceData]):
        facts = []
        for instance_data in instance_datas:
            for s_idx, tuple_graph in instance_data.per_state_tuple_graphs.s_idx_to_tuple_graph.items():
                for d, s_prime_idxs in enumerate(tuple_graph.get_state_indices_by_distance()):
                    for s_prime_idx in s_prime_idxs:
                        facts.append(("s_distance", [Number(instance_data.id), Number(s_idx), Number(s_prime_idx), Number(d)]))
        return facts

    def make_facts(self, domain_data: DomainData, instance_datas: List[InstanceData]):
        facts = []
        facts.extend(self.make_state_space_facts(instance_datas))
        facts.extend(self.make_domain_feature_data_facts(domain_data))
        facts.extend(self.make_instance_feature_data_facts(domain_data, instance_datas))
        facts.extend(self.make_state_pair_equivalence_data_facts(domain_data, instance_datas))
        facts.extend(self.make_tuple_graph_equivalence_facts(domain_data, instance_datas))
        facts.extend(self.make_tuple_graph_facts(domain_data, instance_datas))
        return facts

    def make_initial_d2_facts(self, instance_datas: List[InstanceData]):
        """ T_0 facts """
        facts = set()
        for instance_data in instance_datas:
            for s_idx, tuple_graph in instance_data.per_state_tuple_graphs.s_idx_to_tuple_graph.items():
                if not instance_data.is_alive(s_idx):
                    continue
                equivalences = set()
                for s_prime_idxs in tuple_graph.get_state_indices_by_distance():
                    for s_prime_idx in s_prime_idxs:
                        equivalences.add(instance_data.per_state_state_pair_equivalences.s_idx_to_state_pair_equivalence[s_idx].subgoal_state_to_r_idx[s_prime_idx])
                for i, eq_1 in enumerate(equivalences):
                    for j, eq_2 in enumerate(equivalences):
                        if i < j:
                            facts.add(("d2_separate", (Number(eq_1), Number(eq_2))))
        return facts

    def make_unsatisfied_d2_facts(self, domain_data: DomainData, symbols: List[Symbol]):
        # compute good and bad equivalences
        good_equivalences = set()
        for symbol in symbols:
            if symbol.name == "good":
                good_equivalences.add(symbol.arguments[0].number)
        bad_equivalences = set(r_idx for r_idx in range(len(domain_data.domain_state_pair_equivalence.rules)) if r_idx not in good_equivalences)
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
                r_idx = symbol.arguments[0].number
                f_idx = symbol.arguments[1].number
                condition = symbol.arguments[2].number
                rule_to_feature_to_condition[r_idx][f_idx] = condition
            if symbol.name == "feature_effect":
                r_idx = symbol.arguments[0].number
                f_idx = symbol.arguments[1].number
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
        """ https://potassco.org/clingo/python-api/current/clingo/solving.html """
        with self.ctl.solve(yield_=True) as handle:
            last_model = None
            for model in handle:
                last_model = model
            if last_model is not None:
                assert last_model.optimality_proven
                return last_model.symbols(shown=True), ClingoExitCode.SATISFIABLE
            result = handle.get()
            if result.exhausted:
                return None, ClingoExitCode.EXHAUSTED
            elif result.unsatisfiable:
                return None, ClingoExitCode.UNSATISFIABLE
            elif result.unknown:
                return None, ClingoExitCode.UNKNOWN
            elif result.interrupted:
                return None, ClingoExitCode.INTERRUPTED

    def print_statistics(self):
        print("Clingo statistics:")
        print(self.ctl.statistics["summary"])
        print("Solution cost:", self.ctl.statistics["summary"]["costs"])  # Note: we add +1 cost to each feature
        print("Total time:", self.ctl.statistics["summary"]["times"]["total"])
        print("CPU time:", self.ctl.statistics["summary"]["times"]["cpu"])
        print("Solve time:", self.ctl.statistics["summary"]["times"]["solve"])
