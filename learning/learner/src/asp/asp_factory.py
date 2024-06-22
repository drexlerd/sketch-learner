import os

from collections import defaultdict
from typing import List, Union
from pathlib import Path

from dlplan.core import Boolean, Numerical
from dlplan.policy import PositiveBooleanCondition, NegativeBooleanCondition, GreaterNumericalCondition, EqualNumericalCondition, PositiveBooleanEffect, NegativeBooleanEffect, UnchangedBooleanEffect, DecrementNumericalEffect, IncrementNumericalEffect, UnchangedNumericalEffect

from clingo import Control, Number, Symbol, String

from .returncodes import ClingoExitCode
from .encoding_type import EncodingType

from ..domain_data.domain_data import DomainData
from ..instance_data.instance_data import InstanceData


LIST_DIR = Path(os.path.dirname(os.path.abspath(__file__)))


class ASPFactory:
    def __init__(self, encoding_type: EncodingType, enable_goal_separating_features: bool, max_num_rules: int):
        add_arguments = []
        if encoding_type == EncodingType.EXPLICIT:
            add_arguments.extend(["--const", f"max_num_rules={max_num_rules}"])

        self.ctl = Control(arguments=["--parallel-mode=32,split", "-n", "0"] + add_arguments)

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

        if encoding_type == EncodingType.D2:
            self.ctl.load(str(LIST_DIR / "sketch-d2.lp"))
        elif encoding_type == EncodingType.EXPLICIT:
            self.ctl.load(str(LIST_DIR / "sketch-explicit.lp"))
        else:
            raise RuntimeError("Unknown encoding type:", encoding_type)

        if enable_goal_separating_features:
            self.ctl.load(str(LIST_DIR / "goal_separation.lp"))


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

    def _make_state_space_facts(self, instance_datas: List[InstanceData]):
        """ Create facts that encode the state space.
        """
        facts = []
        for instance_data in instance_datas:
            for s_idx in instance_data.initial_global_s_idxs:
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

    def _make_domain_feature_data_facts(self, domain_data: DomainData):
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


    def _create_value_fact(self, instance_id: int, s_idx: int, f_idx: int, val: Union[bool, int]):
        return ("value", [Number(instance_id), Number(s_idx), Number(f_idx), Number(val)])

    def _create_b_value_fact(self, dlplan_feature: Union[Boolean, Numerical], instance_id: int, s_idx: int, f_idx: int, val: Union[bool, int]):
        if isinstance(dlplan_feature, Boolean):
            return ("b_value", [Number(instance_id), Number(s_idx), Number(f_idx), Number(val)])
        elif isinstance(dlplan_feature, Numerical):
            return ("b_value", [Number(instance_id), Number(s_idx), Number(f_idx), Number(1 if val > 0 else 0)])
        else:
            raise RuntimeError("Expected Boolean or Numerical feature.")

    def _make_instance_feature_data_facts(self, domain_data: DomainData, instance_datas: List[InstanceData]):
        facts = []
        # Instance feature valuation facts
        feature_pool = domain_data.feature_pool
        for instance_data in instance_datas:
            for s_idx in instance_data.state_space.get_states().keys():
                feature_valuation = instance_data.per_state_feature_valuations.s_idx_to_feature_valuations[s_idx]
                for f_idx, (feature, val) in enumerate(zip(feature_pool.features, feature_valuation.feature_valuations)):
                    facts.append(self._create_value_fact(instance_data.id, s_idx, f_idx, val))
                    facts.append(self._create_b_value_fact(feature.dlplan_feature, instance_data.id, s_idx, f_idx, val))
        return facts


    def _create_state_pair_class_fact(self, r_idx: int):
        return ("state_pair_class", [Number(r_idx)])

    def _create_feature_condition_fact(self, condition: Union[PositiveBooleanCondition, NegativeBooleanCondition, GreaterNumericalCondition, EqualNumericalCondition], r_idx: int, f_idx: int):
        if isinstance(condition, PositiveBooleanCondition):
            return ("feature_condition", [Number(r_idx), Number(f_idx), String("c_b_pos")])
        elif isinstance(condition, NegativeBooleanCondition):
            return ("feature_condition", [Number(r_idx), Number(f_idx), String("c_b_neg")])
        elif isinstance(condition, GreaterNumericalCondition):
            return ("feature_condition", [Number(r_idx), Number(f_idx), String("c_n_gt")])
        elif isinstance(condition, EqualNumericalCondition):
            return ("feature_condition", [Number(r_idx), Number(f_idx), String("c_n_eq")])
        else:
            raise RuntimeError(f"Cannot parse condition {str(condition)}")

    def _create_feature_effect_fact(self, effect: Union[PositiveBooleanEffect, NegativeBooleanEffect, UnchangedBooleanEffect, IncrementNumericalEffect, DecrementNumericalEffect, UnchangedNumericalEffect], r_idx: int, f_idx: int):
        if isinstance(effect, PositiveBooleanEffect):
            return ("feature_effect", [Number(r_idx), Number(f_idx), String("e_b_pos")])
        elif isinstance(effect, NegativeBooleanEffect):
            return ("feature_effect", [Number(r_idx), Number(f_idx), String("e_b_neg")])
        elif isinstance(effect, UnchangedBooleanEffect):
            return ("feature_effect", [Number(r_idx), Number(f_idx), String("e_b_bot")])
        elif isinstance(effect, IncrementNumericalEffect):
            return ("feature_effect", [Number(r_idx), Number(f_idx), String("e_n_inc")])
        elif isinstance(effect, DecrementNumericalEffect):
            return ("feature_effect", [Number(r_idx), Number(f_idx), String("e_n_dec")])
        elif isinstance(effect, UnchangedNumericalEffect):
            return ("feature_effect", [Number(r_idx), Number(f_idx), String("e_n_bot")])
        else:
            raise RuntimeError(f"Cannot parse effect {str(effect)}")

    def _create_r_distance_fact(self, instance_id: int, s_idx: int, r_idx: int, d: int):
        return ("r_distance", [Number(instance_id), Number(s_idx), Number(r_idx), Number(d)])

    def _create_cover_fact(self, instance_id: int, s_idx: int, s_prime_idx: int, r_idx: int):
        return ("cover", [Number(instance_id), Number(s_idx), Number(s_prime_idx), Number(r_idx)])

    def _make_state_pair_equivalence_data_facts(self, domain_data: DomainData, instance_datas: List[InstanceData]):
        facts = []
        # State pair facts
        for r_idx, rule in enumerate(domain_data.domain_state_pair_equivalence.rules):
            facts.append(self._create_state_pair_class_fact(r_idx))
            for condition in rule.get_conditions():
                f_idx = int(condition.get_named_element().get_key()[1:])
                facts.append(self._create_feature_condition_fact(condition, r_idx, f_idx))
            for effect in rule.get_effects():
                f_idx = int(effect.get_named_element().get_key()[1:])
                facts.append(self._create_feature_effect_fact(effect, r_idx, f_idx))
        # State pair equivalence facts
        for instance_data in instance_datas:
            for s_idx, state_pair_equivalence in instance_data.per_state_state_pair_equivalences.s_idx_to_state_pair_equivalence.items():
                if instance_data.is_deadend(s_idx):
                    continue
                for r_idx, d in state_pair_equivalence.r_idx_to_distance.items():
                    facts.append(self._create_r_distance_fact(instance_data.id, s_idx, r_idx, d))
                for r_idx, s_prime_idxs in state_pair_equivalence.r_idx_to_subgoal_states.items():
                    for s_prime_idx in s_prime_idxs:
                        facts.append(self._create_cover_fact(instance_data.id, s_idx, s_prime_idx, r_idx))
        return facts


    def _create_tuple_fact(self, instance_id: int, s_idx: int, t_idx: int):
        return ("tuple", [Number(instance_id), Number(s_idx), Number(t_idx)])

    def _create_contain_fact(self, instance_id: int, s_idx: int, t_idx: int, r_idx: int):
        return ("contain", [Number(instance_id), Number(s_idx), Number(t_idx), Number(r_idx)])

    def _create_t_distance_fact(self, instance_id: int, s_idx: int, t_idx: int, d: int):
        return ("t_distance", [Number(instance_id), Number(s_idx), Number(t_idx), Number(d)])

    def _create_d_distance_fact(self, instance_id: int, s_idx: int, r_idx: int, d: int):
        return ("d_distance", [Number(instance_id), Number(s_idx), Number(r_idx), Number(d)])

    def _make_tuple_graph_equivalence_facts(self, domain_data: DomainData, instance_datas: List[InstanceData]):
        facts = []
        # Tuple graph equivalence facts (Perhaps deprecated since we now let rules imply subgoals)
        for instance_data in instance_datas:
            for s_idx, tuple_graph_equivalence in instance_data.per_state_tuple_graph_equivalences.s_idx_to_tuple_graph_equivalence.items():
                if instance_data.is_deadend(s_idx):
                    continue
                for t_idx, r_idxs in tuple_graph_equivalence.t_idx_to_r_idxs.items():
                    facts.append(self._create_tuple_fact(instance_data.id, s_idx, t_idx))
                    for r_idx in r_idxs:
                        facts.append(self._create_contain_fact(instance_data.id, s_idx, t_idx, r_idx))
                for t_idx, d in tuple_graph_equivalence.t_idx_to_distance.items():
                    facts.append(self._create_t_distance_fact(instance_data.id, s_idx, t_idx, d))
                for r_idx, d in tuple_graph_equivalence.r_idx_to_deadend_distance.items():
                    facts.append(self._create_d_distance_fact(instance_data.id, s_idx, r_idx, d))
        return facts


    def _create_s_distance_fact(self, instance_id: int, s_idx: int, s_prime_idx: int, d: int):
        return ("s_distance", [Number(instance_id), Number(s_idx), Number(s_prime_idx), Number(d)])

    def _make_tuple_graph_facts(self, domain_data: DomainData, instance_datas: List[InstanceData]):
        facts = []
        for instance_data in instance_datas:
            for s_idx, tuple_graph in instance_data.per_state_tuple_graphs.s_idx_to_tuple_graph.items():
                for d, s_prime_idxs in enumerate(tuple_graph.get_state_indices_by_distance()):
                    for s_prime_idx in set(instance_data.concrete_s_idx_to_global_s_idx[s] for s in s_prime_idxs):
                        facts.append(self._create_s_distance_fact(instance_data.id, s_idx, s_prime_idx, d))
        return facts


    def make_facts(self, domain_data: DomainData, instance_datas: List[InstanceData]):
        facts = []
        facts.extend(self._make_state_space_facts(instance_datas))
        facts.extend(self._make_domain_feature_data_facts(domain_data))
        facts.extend(self._make_instance_feature_data_facts(domain_data, instance_datas))
        facts.extend(self._make_state_pair_equivalence_data_facts(domain_data, instance_datas))
        facts.extend(self._make_tuple_graph_equivalence_facts(domain_data, instance_datas))
        facts.extend(self._make_tuple_graph_facts(domain_data, instance_datas))
        return facts

    def _create_d2_separate_fact(self, r_idx_1: int, r_idx_2: int):
        return ("d2_separate", (Number(r_idx_1), Number(r_idx_2)))

    def make_initial_d2_facts(self, instance_datas: List[InstanceData]):
        """ T_0 facts """
        facts = set()
        for instance_data in instance_datas:
            for s_idx, tuple_graph in instance_data.per_state_tuple_graphs.s_idx_to_tuple_graph.items():
                if not instance_data.is_alive(s_idx):
                    continue
                equivalences = set()
                for s_prime_idxs in tuple_graph.get_state_indices_by_distance():
                    for s_prime_idx in set(instance_data.concrete_s_idx_to_global_s_idx[s] for s in s_prime_idxs):
                        equivalences.add(instance_data.per_state_state_pair_equivalences.s_idx_to_state_pair_equivalence[s_idx].subgoal_state_to_r_idx[s_prime_idx])
                for i, eq_1 in enumerate(equivalences):
                    for j, eq_2 in enumerate(equivalences):
                        if i < j:
                            facts.add(self._create_d2_separate_fact(eq_1, eq_2))
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
                condition = symbol.arguments[2].string
                rule_to_feature_to_condition[r_idx][f_idx] = condition
            if symbol.name == "feature_effect":
                r_idx = symbol.arguments[0].number
                f_idx = symbol.arguments[1].number
                effect = symbol.arguments[2].string
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
                    facts.add(self._create_d2_separate_fact(good, bad))
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
