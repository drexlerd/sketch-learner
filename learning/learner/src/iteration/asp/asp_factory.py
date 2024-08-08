import os

from collections import defaultdict
from typing import List, Union, Dict
from pathlib import Path

import pymimir as mm

import dlplan.core as dlplan_core
import dlplan.policy as dlplan_policy

from clingo import Control, Number, Symbol, String

from .returncodes import ClingoExitCode
from .encoding_type import EncodingType

from ...preprocessing.preprocessing_data import PreprocessingData
from ..iteration_data import IterationData


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

    def _make_state_space_facts(self, preprocessing_data: PreprocessingData,
                                iteration_data: IterationData):
        """ Create facts that encode the state space.
        """
        facts = []
        for instance_data in iteration_data.instance_datas:
            for s_idx in instance_data.initial_ss_state_idxs:
                facts.append(self._create_initial_fact(instance_data.idx, s_idx))
            for s_idx in range(instance_data.mimir_ss.get_num_states()):
                facts.append(self._create_state_fact(instance_data.idx, s_idx))
                if not instance_data.mimir_ss.is_deadend_state(s_idx):
                    facts.append(self._create_solvable_fact(instance_data.idx, s_idx))
                else:
                    facts.append(self._create_unsolvable_fact(instance_data.idx, s_idx))
                if instance_data.mimir_ss.is_goal_state(s_idx):
                    facts.append(self._create_goal_fact(instance_data.idx, s_idx))
                else:
                    facts.append(self._create_nongoal_fact(instance_data.idx, s_idx))
                if instance_data.mimir_ss.is_alive_state(s_idx):
                    facts.append(self._create_alive_fact(instance_data.idx, s_idx))
        return sorted(list(facts))

    def _create_feature_fact(self, f_idx: int):
        return ("feature", (Number(f_idx),))

    def _create_complexity_fact(self, f_idx: int, complexity: int):
        return ("complexity", (Number(f_idx), Number(complexity),))

    def _create_boolean_fact(self, f_idx: int):
        return ("boolean", (Number(f_idx),))

    def _create_numerical_fact(self, f_idx: int):
        return ("numerical", (Number(f_idx),))

    def _make_domain_feature_data_facts(self,
                                        preprocessing_data: PreprocessingData,
                                        iteration_data: IterationData):
        facts = []
        # Domain feature facts
        for f_idx, feature in enumerate(iteration_data.feature_pool):
            facts.append(self._create_feature_fact(f_idx))
            facts.append(self._create_complexity_fact(f_idx, feature.complexity))
            if isinstance(feature.dlplan_feature, dlplan_core.Boolean):
                facts.append(self._create_boolean_fact(f_idx))
            elif isinstance(feature.dlplan_feature, dlplan_core.Numerical):
                facts.append(self._create_numerical_fact(f_idx))
        return facts

    def _create_value_fact(self, instance_id: int, s_idx: int, f_idx: int, val: Union[bool, int]):
        return ("value", [Number(instance_id), Number(s_idx), Number(f_idx), Number(val)])

    def _create_b_value_fact(self, dlplan_feature: Union[dlplan_core.Boolean, dlplan_core.Numerical], instance_id: int, s_idx: int, f_idx: int, val: Union[bool, int]):
        if isinstance(dlplan_feature, dlplan_core.Boolean):
            return ("b_value", [Number(instance_id), Number(s_idx), Number(f_idx), Number(val)])
        elif isinstance(dlplan_feature, dlplan_core.Numerical):
            return ("b_value", [Number(instance_id), Number(s_idx), Number(f_idx), Number(1 if val > 0 else 0)])
        else:
            raise RuntimeError("Expected Boolean or Numerical feature.")

    def _make_instance_feature_data_facts(self,
                                          preprocessing_data: PreprocessingData,
                                          iteration_data: IterationData):
        facts = []
        # Instance feature valuation facts
        feature_pool = iteration_data.feature_pool
        for instance_data in iteration_data.instance_datas:
            for mimir_ss_state_idx in range(instance_data.mimir_ss.get_num_states()):
                feature_valuations = iteration_data.instance_idx_to_ss_idx_to_feature_valuations[instance_data.idx][mimir_ss_state_idx]
                for f_idx, (feature, val) in enumerate(zip(feature_pool, feature_valuations)):
                    facts.append(self._create_value_fact(instance_data.idx, mimir_ss_state_idx, f_idx, val))
                    facts.append(self._create_b_value_fact(feature.dlplan_feature, instance_data.idx, mimir_ss_state_idx, f_idx, val))
        return facts


    def _create_state_pair_class_fact(self, r_idx: int):
        return ("state_pair_class", (Number(r_idx),))

    def _create_feature_condition_fact(self, condition: Union[dlplan_policy.PositiveBooleanCondition, dlplan_policy.NegativeBooleanCondition, dlplan_policy.GreaterNumericalCondition, dlplan_policy.EqualNumericalCondition], r_idx: int, f_idx: int):
        if isinstance(condition, dlplan_policy.PositiveBooleanCondition):
            return ("feature_condition", (Number(r_idx), Number(f_idx), String("c_b_pos"),))
        elif isinstance(condition, dlplan_policy.NegativeBooleanCondition):
            return ("feature_condition", (Number(r_idx), Number(f_idx), String("c_b_neg"),))
        elif isinstance(condition, dlplan_policy.GreaterNumericalCondition):
            return ("feature_condition", (Number(r_idx), Number(f_idx), String("c_n_gt"),))
        elif isinstance(condition, dlplan_policy.EqualNumericalCondition):
            return ("feature_condition", (Number(r_idx), Number(f_idx), String("c_n_eq"),))
        else:
            raise RuntimeError(f"Cannot parse condition {str(condition)}")

    def _create_feature_effect_fact(self, effect: Union[dlplan_policy.PositiveBooleanEffect, dlplan_policy.NegativeBooleanEffect, dlplan_policy.UnchangedBooleanEffect, dlplan_policy.IncrementNumericalEffect, dlplan_policy.DecrementNumericalEffect, dlplan_policy.UnchangedNumericalEffect], r_idx: int, f_idx: int):
        if isinstance(effect, dlplan_policy.PositiveBooleanEffect):
            return ("feature_effect", (Number(r_idx), Number(f_idx), String("e_b_pos"),))
        elif isinstance(effect, dlplan_policy.NegativeBooleanEffect):
            return ("feature_effect", (Number(r_idx), Number(f_idx), String("e_b_neg"),))
        elif isinstance(effect, dlplan_policy.UnchangedBooleanEffect):
            return ("feature_effect", (Number(r_idx), Number(f_idx), String("e_b_bot"),))
        elif isinstance(effect, dlplan_policy.IncrementNumericalEffect):
            return ("feature_effect", (Number(r_idx), Number(f_idx), String("e_n_inc"),))
        elif isinstance(effect, dlplan_policy.DecrementNumericalEffect):
            return ("feature_effect", (Number(r_idx), Number(f_idx), String("e_n_dec"),))
        elif isinstance(effect, dlplan_policy.UnchangedNumericalEffect):
            return ("feature_effect", (Number(r_idx), Number(f_idx), String("e_n_bot"),))
        else:
            raise RuntimeError(f"Cannot parse effect {str(effect)}")

    def _create_r_distance_fact(self, instance_id: int, s_idx: int, r_idx: int, d: int):
        return ("r_distance", [Number(instance_id), Number(s_idx), Number(r_idx), Number(d)])

    def _create_cover_fact(self, instance_id: int, s_idx: int, s_prime_idx: int, r_idx: int):
        return ("cover", [Number(instance_id), Number(s_idx), Number(s_prime_idx), Number(r_idx)])

    def _make_state_pair_equivalence_data_facts(self,
                                                preprocessing_data: PreprocessingData,
                                                iteration_data: IterationData):
        facts = []
        # State pair facts
        for r_idx, rule in enumerate(iteration_data.state_pair_equivalences):
            facts.append(self._create_state_pair_class_fact(r_idx))
            for condition in rule.get_conditions():
                f_idx = int(condition.get_named_element().get_key()[1:])
                facts.append(self._create_feature_condition_fact(condition, r_idx, f_idx))
            for effect in rule.get_effects():
                f_idx = int(effect.get_named_element().get_key()[1:])
                facts.append(self._create_feature_effect_fact(effect, r_idx, f_idx))
        # State pair equivalence facts
        for instance_data in iteration_data.instance_datas:
            for mimir_ss_state_idx, state_pair_equivalence in iteration_data.instance_idx_to_ss_idx_to_state_pair_equivalence[instance_data.idx].items():
                for r_idx, d in state_pair_equivalence.r_idx_to_closest_subgoal_distance.items():
                    facts.append(self._create_r_distance_fact(instance_data.idx, mimir_ss_state_idx, r_idx, d))
                for r_idx, gfa_state_prime_ids in state_pair_equivalence.r_idx_to_subgoal_gfa_state_ids.items():
                    for gfa_state_prime_id in gfa_state_prime_ids:
                        facts.append(self._create_cover_fact(instance_data.idx, mimir_ss_state_idx, gfa_state_prime_id, r_idx))
        return facts

    def _create_tuple_fact(self, instance_id: int, s_idx: int, t_idx: int):
        return ("tuple", [Number(instance_id), Number(s_idx), Number(t_idx)])

    def _create_contain_fact(self, instance_id: int, s_idx: int, t_idx: int, r_idx: int):
        return ("contain", [Number(instance_id), Number(s_idx), Number(t_idx), Number(r_idx)])

    def _create_t_distance_fact(self, instance_id: int, s_idx: int, t_idx: int, d: int):
        return ("t_distance", [Number(instance_id), Number(s_idx), Number(t_idx), Number(d)])

    def _create_d_distance_fact(self, instance_id: int, s_idx: int, r_idx: int, d: int):
        return ("d_distance", [Number(instance_id), Number(s_idx), Number(r_idx), Number(d)])

    def _make_tuple_graph_equivalence_facts(self,
                                            preprocessing_data: PreprocessingData,
                                            iteration_data: IterationData):
        facts = []
        for instance_data in iteration_data.instance_datas:
            for mimir_ss_state_idx, tuple_graph_equivalence in iteration_data.instance_idx_to_ss_idx_to_tuple_graph_equivalence[instance_data.idx].items():
                for t_idx, r_idxs in tuple_graph_equivalence.t_idx_to_r_idxs.items():
                    facts.append(self._create_tuple_fact(instance_data.idx, mimir_ss_state_idx, t_idx))
                    for r_idx in r_idxs:
                        facts.append(self._create_contain_fact(instance_data.idx, mimir_ss_state_idx, t_idx, r_idx))
                for t_idx, d in tuple_graph_equivalence.t_idx_to_distance.items():
                    facts.append(self._create_t_distance_fact(instance_data.idx, mimir_ss_state_idx, t_idx, d))
                for r_idx, d in tuple_graph_equivalence.r_idx_to_deadend_distance.items():
                    facts.append(self._create_d_distance_fact(instance_data.idx, mimir_ss_state_idx, r_idx, d))
        return facts


    def _create_s_distance_fact(self, instance_id: int, s_idx: int, s_prime_idx: int, d: int):
        return ("s_distance", [Number(instance_id), Number(s_idx), Number(s_prime_idx), Number(d)])

    def _make_tuple_graph_facts(self,
                                preprocessing_data: PreprocessingData,
                                iteration_data: IterationData):
        facts = []
        for instance_data in iteration_data.instance_datas:
            for mimir_ss_state_idx, tuple_graph in preprocessing_data.ss_state_idx_to_tuple_graph[instance_data.idx].items():
                tuple_graph_states_by_distance = tuple_graph.get_states_grouped_by_distance()

                for s_distance, mimir_ss_states_prime in enumerate(tuple_graph_states_by_distance):
                    for mimir_ss_state_prime in mimir_ss_states_prime:
                        mimir_ss_state_prime_idx = instance_data.mimir_ss.get_state_index(mimir_ss_state_prime)
                        facts.append(self._create_s_distance_fact(instance_data.idx, mimir_ss_state_idx, mimir_ss_state_prime_idx, s_distance))

        return facts


    def make_facts(self,
                   preprocessing_data: PreprocessingData,
                   iteration_data: IterationData):
        facts = []
        facts.extend(self._make_state_space_facts(preprocessing_data, iteration_data))
        facts.extend(self._make_domain_feature_data_facts(preprocessing_data, iteration_data))
        facts.extend(self._make_instance_feature_data_facts(preprocessing_data, iteration_data))
        facts.extend(self._make_state_pair_equivalence_data_facts(preprocessing_data, iteration_data))
        facts.extend(self._make_tuple_graph_equivalence_facts(preprocessing_data, iteration_data))
        facts.extend(self._make_tuple_graph_facts(preprocessing_data, iteration_data))
        return facts

    def _create_d2_separate_fact(self, r_idx_1: int, r_idx_2: int):
        return ("d2_separate", (Number(r_idx_1), Number(r_idx_2)))

    def make_initial_d2_facts(self,
                              preprocessing_data: PreprocessingData,
                              iteration_data: IterationData):
        """ T_0 facts """
        facts = set()
        for instance_data in iteration_data.instance_datas:
            for mimir_ss_state_idx, tuple_graph in preprocessing_data.ss_state_idx_to_tuple_graph[instance_data.idx].items():
                tuple_graph_vertices_by_distance = tuple_graph.get_vertices_grouped_by_distance()

                equivalences = set()

                for tuple_vertex_group in tuple_graph_vertices_by_distance:
                    for tuple_vertex in tuple_vertex_group:
                        for mimir_ss_state_prime in tuple_vertex.get_states():
                            mimir_ss_state_prime_idx = instance_data.mimir_ss.get_state_index(mimir_ss_state_prime)

                            equivalences.add(iteration_data.instance_idx_to_ss_idx_to_state_pair_equivalence[instance_data.idx][mimir_ss_state_idx].subgoal_gfa_state_id_to_r_idx[mimir_ss_state_prime_idx])

                for i, eq_1 in enumerate(equivalences):
                    for j, eq_2 in enumerate(equivalences):
                        if i < j:
                            facts.add(self._create_d2_separate_fact(eq_1, eq_2))
        return facts

    def make_unsatisfied_d2_facts(self, iteration_data: IterationData, symbols: List[Symbol]):
        # compute good and bad equivalences
        good_equivalences = set()
        for symbol in symbols:
            if symbol.name == "good":
                good_equivalences.add(symbol.arguments[0].number)
        bad_equivalences = set(r_idx for r_idx in range(len(iteration_data.state_pair_equivalences)) if r_idx not in good_equivalences)
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
