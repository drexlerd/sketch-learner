import os

from collections import defaultdict
from typing import List, Union
from pathlib import Path

import dlplan.core as dlplan_core
import dlplan.policy as dlplan_policy

from clingo import Control, Number, Symbol, String

from .returncodes import ClingoExitCode
from .encoding_type import EncodingType

from ..domain_data.domain_data import DomainData
from ..instance_data.instance_data import InstanceData, StateFinder


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
        self.ctl.add("value", ["s","f","v"], "value(s,f,v).")
        self.ctl.add("b_value", ["s","f","v"], "b_value(s,f,v).")
        # state space
        self.ctl.add("state", ["s"], "state(s).")
        self.ctl.add("initial", ["s"], "initial(s).")
        self.ctl.add("solvable", ["s"], "solvable(s).")
        self.ctl.add("unsolvable", ["s"], "unsolvable(s).")
        self.ctl.add("goal", ["s"], "goal(s).")
        self.ctl.add("nongoal", ["s"], "nongoal(s).")
        self.ctl.add("alive", ["s"], "alive(s).")
        self.ctl.add("expanded", ["s"], "expanded(s).")
        # rule equivalences
        self.ctl.add("feature_condition", ["r", "f", "v"], "feature_condition(r,f,v).")
        self.ctl.add("feature_effect", ["r", "f", "v"], "feature_effect(r,f,v).")
        self.ctl.add("state_pair_class", ["r"], "state_pair_class(r).")
        # d2-separation constraints
        self.ctl.add("d2_separate", ["r1", "r2"], "d2_separate(r1,r2).")
        # tuple graph
        self.ctl.add("tuple", ["s", "t"], "tuple(s,t).")
        self.ctl.add("contain", ["s", "t", "r"], "contain(s,t,r).")
        self.ctl.add("cover", ["s1", "s2", "r"], "cover(s1,s2,r).")
        self.ctl.add("t_distance", ["s", "t", "d"], "t_distance(s,t,d).")
        self.ctl.add("d_distance", ["s", "r", "d"], "d_distance(s,r,d).")
        self.ctl.add("r_distance", ["s", "r", "d"], "r_distance(s,r,d).")
        self.ctl.add("s_distance", ["s1", "s2", "d"], "s_distance(s1,s2,d).")

        if encoding_type == EncodingType.D2:
            self.ctl.load(str(LIST_DIR / "sketch-d2.lp"))
        elif encoding_type == EncodingType.EXPLICIT:
            self.ctl.load(str(LIST_DIR / "sketch-explicit.lp"))
        else:
            raise RuntimeError("Unknown encoding type:", encoding_type)

        if enable_goal_separating_features:
            self.ctl.load(str(LIST_DIR / "goal_separation.lp"))


    def _create_initial_fact(self, gfa_state_id: int):
        return ("initial", (Number(gfa_state_id),))

    def _create_state_fact(self, gfa_state_id: int):
        return ("state", (Number(gfa_state_id),))

    def _create_solvable_fact(self, gfa_state_id: int):
        return ("solvable", (Number(gfa_state_id),))

    def _create_unsolvable_fact(self, gfa_state_id: int):
        return ("unsolvable", (Number(gfa_state_id),))

    def _create_goal_fact(self, gfa_state_id: int):
        return ("goal", (Number(gfa_state_id),))

    def _create_nongoal_fact(self, gfa_state_id: int):
        return ("nongoal", (Number(gfa_state_id),))

    def _create_alive_fact(self, gfa_state_id: int):
        return ("alive", (Number(gfa_state_id),))

    def _make_state_space_facts(self, domain_data: DomainData, instance_datas: List[InstanceData], selected_instance_datas: List[InstanceData], state_finder: StateFinder):
        """ Create facts that encode the state space.
        """
        facts = set()
        for instance_data in selected_instance_datas:
            for initial_gfa_idx in instance_data.initial_gfa_state_idxs:
                initial_gfa_state = instance_data.gfa.get_states()[initial_gfa_idx]
                initial_gfa_state_id = initial_gfa_state.get_id()
                facts.add(self._create_initial_fact(initial_gfa_state_id))
            for gfa_state in instance_data.gfa.get_states():
                gfa_state_id = gfa_state.get_id()
                gfa_state_idx = instance_data.gfa.get_state_index(gfa_state)
                facts.add(self._create_state_fact(gfa_state_id))
                if not instance_data.gfa.is_deadend_state(gfa_state_idx):
                    facts.add(self._create_solvable_fact(gfa_state_id))
                else:
                    facts.add(self._create_unsolvable_fact(gfa_state_id))
                if instance_data.gfa.is_goal_state(gfa_state_idx):
                    facts.add(self._create_goal_fact(gfa_state_id))
                else:
                    facts.add(self._create_nongoal_fact(gfa_state_id))
                if instance_data.gfa.is_alive_state(gfa_state_idx):
                    facts.add(self._create_alive_fact(gfa_state_id))
        return sorted(list(facts))


    def _create_feature_fact(self, f_idx: int):
        return ("feature", (Number(f_idx),))

    def _create_complexity_fact(self, f_idx: int, complexity: int):
        return ("complexity", (Number(f_idx), Number(complexity),))

    def _create_boolean_fact(self, f_idx: int):
        return ("boolean", (Number(f_idx),))

    def _create_numerical_fact(self, f_idx: int):
        return ("numerical", (Number(f_idx),))

    def _make_domain_feature_data_facts(self, domain_data: DomainData, instance_datas: List[InstanceData], selected_instance_datas: List[InstanceData], state_finder: StateFinder):
        facts = []
        # Domain feature facts
        for f_idx, feature in enumerate(domain_data.feature_pool):
            facts.append(self._create_feature_fact(f_idx))
            facts.append(self._create_complexity_fact(f_idx, feature.complexity))
            if isinstance(feature.dlplan_feature, dlplan_core.Boolean):
                facts.append(self._create_boolean_fact(f_idx))
            elif isinstance(feature.dlplan_feature, dlplan_core.Numerical):
                facts.append(self._create_numerical_fact(f_idx))
        return facts


    def _create_value_fact(self, gfa_state_id: int, f_idx: int, val: Union[bool, int]):
        return ("value", (Number(gfa_state_id), Number(f_idx), Number(val)))

    def _create_b_value_fact(self, dlplan_feature: Union[dlplan_core.Boolean, dlplan_core.Numerical], gfa_state_id: int, f_idx: int, val: Union[bool, int]):
        if isinstance(dlplan_feature, dlplan_core.Boolean):
            return ("b_value", (Number(gfa_state_id), Number(f_idx), Number(val)))
        elif isinstance(dlplan_feature, dlplan_core.Numerical):
            return ("b_value", (Number(gfa_state_id), Number(f_idx), Number(1 if val > 0 else 0)))
        else:
            raise RuntimeError("Expected Boolean or Numerical feature.")

    def _make_instance_feature_data_facts(self, domain_data: DomainData, instance_datas: List[InstanceData], selected_instance_datas: List[InstanceData], state_finder: StateFinder):
        facts = []
        # Instance feature valuation facts
        feature_pool = domain_data.feature_pool
        for gfa_state_id, feature_valuations in domain_data.gfa_state_id_to_feature_evaluations.items():
            for f_idx, (feature, val) in enumerate(zip(feature_pool, feature_valuations)):
                facts.append(self._create_value_fact(gfa_state_id, f_idx, val))
                facts.append(self._create_b_value_fact(feature.dlplan_feature, gfa_state_id, f_idx, val))
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

    def _create_r_distance_fact(self, gfa_state_id: int, r_idx: int, d: int):
        return ("r_distance", (Number(gfa_state_id), Number(r_idx), Number(d)))

    def _create_cover_fact(self, gfa_state_id: int, gfa_state_prime_id: int, r_idx: int):
        return ("cover", (Number(gfa_state_id), Number(gfa_state_prime_id), Number(r_idx)))

    def _make_state_pair_equivalence_data_facts(self, domain_data: DomainData, instance_datas: List[InstanceData], selected_instance_datas: List[InstanceData], state_finder: StateFinder):
        facts = []
        # State pair facts
        for r_idx, rule in enumerate(domain_data.state_pair_equivalences):
            facts.append(self._create_state_pair_class_fact(r_idx))
            for condition in rule.get_conditions():
                f_idx = int(condition.get_named_element().get_key()[1:])
                facts.append(self._create_feature_condition_fact(condition, r_idx, f_idx))
            for effect in rule.get_effects():
                f_idx = int(effect.get_named_element().get_key()[1:])
                facts.append(self._create_feature_effect_fact(effect, r_idx, f_idx))
        # State pair equivalence facts
        for gfa_state_id, state_pair_equivalence in domain_data.gfa_state_id_to_state_pair_equivalence.items():
            for r_idx, d in state_pair_equivalence.r_idx_to_closest_subgoal_distance.items():
                facts.append(self._create_r_distance_fact(gfa_state_id, r_idx, d))
            for r_idx, gfa_state_prime_ids in state_pair_equivalence.r_idx_to_subgoal_gfa_state_ids.items():
                for gfa_state_prime_id in gfa_state_prime_ids:
                    facts.append(self._create_cover_fact(gfa_state_id, gfa_state_prime_id, r_idx))
        return facts


    def _create_tuple_fact(self, gfa_state_id: int, t_idx: int):
        return ("tuple", (Number(gfa_state_id), Number(t_idx)))

    def _create_contain_fact(self, gfa_state_id: int, t_idx: int, r_idx: int):
        return ("contain", (Number(gfa_state_id), Number(t_idx), Number(r_idx)))

    def _create_t_distance_fact(self, gfa_state_id: int, t_idx: int, d: int):
        return ("t_distance", (Number(gfa_state_id), Number(t_idx), Number(d)))

    def _create_d_distance_fact(self, gfa_state_id: int, r_idx: int, d: int):
        return ("d_distance", (Number(gfa_state_id), Number(r_idx), Number(d)))

    def _make_tuple_graph_equivalence_facts(self, domain_data: DomainData, instance_datas: List[InstanceData], selected_instance_datas: List[InstanceData], state_finder: StateFinder):
        facts = []
        for gfa_state_id, tuple_graph_equivalence in domain_data.gfa_state_id_to_tuple_graph_equivalence.items():
            for t_idx, r_idxs in tuple_graph_equivalence.t_idx_to_r_idxs.items():
                facts.append(self._create_tuple_fact(gfa_state_id, t_idx))
                for r_idx in r_idxs:
                    facts.append(self._create_contain_fact(gfa_state_id, t_idx, r_idx))
            for t_idx, d in tuple_graph_equivalence.t_idx_to_distance.items():
                facts.append(self._create_t_distance_fact(gfa_state_id, t_idx, d))
            for r_idx, d in tuple_graph_equivalence.r_idx_to_deadend_distance.items():
                facts.append(self._create_d_distance_fact(gfa_state_id, r_idx, d))
        return facts


    def _create_s_distance_fact(self, gfa_state_id: int, gfa_state_prime_id: int, d: int):
        return ("s_distance", (Number(gfa_state_id), Number(gfa_state_prime_id), Number(d)))

    def _make_tuple_graph_facts(self, domain_data: DomainData, instance_datas: List[InstanceData], selected_instance_datas: List[InstanceData], state_finder: StateFinder):
        facts = []
        for gfa_state in domain_data.gfa_states:
            instance_idx = gfa_state.get_abstraction_id()
            instance_data = instance_datas[instance_idx]

            gfa_state_id = gfa_state.get_id()
            gfa_state_idx = state_finder.get_gfa_state_idx_from_gfa_state(gfa_state.get_abstraction_id(), gfa_state)
            if instance_data.gfa.is_deadend_state(gfa_state_idx):
                continue

            tuple_graph = domain_data.gfa_state_id_to_tuple_graph[gfa_state_id]

            for s_distance, mimir_ss_states_prime in enumerate(tuple_graph.get_states_by_distance()):
                for mimir_ss_state_prime in mimir_ss_states_prime:
                    gfa_state_prime = state_finder.get_gfa_state_from_ss_state_idx(instance_idx, instance_data.mimir_ss.get_state_index(mimir_ss_state_prime))
                    gfa_state_prime_id = gfa_state_prime.get_id()
                    facts.append(self._create_s_distance_fact(gfa_state_id, gfa_state_prime_id, s_distance))

        return facts


    def make_facts(self,
                   domain_data: DomainData,
                   instance_datas: List[InstanceData],
                   selected_instance_datas: List[InstanceData],
                   state_finder: StateFinder):
        facts = []
        facts.extend(self._make_state_space_facts(domain_data, instance_datas, selected_instance_datas, state_finder))
        facts.extend(self._make_domain_feature_data_facts(domain_data, instance_datas, selected_instance_datas, state_finder))
        facts.extend(self._make_instance_feature_data_facts(domain_data, instance_datas, selected_instance_datas, state_finder))
        facts.extend(self._make_state_pair_equivalence_data_facts(domain_data, instance_datas, selected_instance_datas, state_finder))
        facts.extend(self._make_tuple_graph_equivalence_facts(domain_data, instance_datas, selected_instance_datas, state_finder))
        facts.extend(self._make_tuple_graph_facts(domain_data, instance_datas, selected_instance_datas, state_finder))
        return facts

    def _create_d2_separate_fact(self, r_idx_1: int, r_idx_2: int):
        return ("d2_separate", (Number(r_idx_1), Number(r_idx_2)))

    def make_initial_d2_facts(self, domain_data: DomainData, instance_datas: List[InstanceData], selected_instance_datas: List[InstanceData], state_finder: StateFinder):
        """ T_0 facts """
        facts = set()
        for gfa_state in domain_data.gfa_states:
            instance_idx = gfa_state.get_abstraction_id()
            instance_data = instance_datas[instance_idx]

            gfa_state_id = gfa_state.get_id()
            gfa_state_idx = state_finder.get_gfa_state_idx_from_gfa_state(gfa_state.get_abstraction_id(), gfa_state)
            if instance_data.gfa.is_deadend_state(gfa_state_idx):
                continue

            tuple_graph = domain_data.gfa_state_id_to_tuple_graph[gfa_state_id]

            equivalences = set()

            for tuple_vertex_idxs in tuple_graph.get_vertex_indices_by_distances():
                for tuple_vertex_idx in tuple_vertex_idxs:
                    tuple_vertex = tuple_graph.get_vertices()[tuple_vertex_idx]
                    for mimir_ss_state_prime in tuple_vertex.get_states():
                        gfa_state_prime = state_finder.get_gfa_state_from_ss_state_idx(instance_idx, instance_data.mimir_ss.get_state_index(mimir_ss_state_prime))
                        gfa_state_prime_id = gfa_state_prime.get_id()
                        equivalences.add(domain_data.gfa_state_id_to_state_pair_equivalence[gfa_state_id].subgoal_gfa_state_id_to_r_idx[gfa_state_prime_id])

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
        bad_equivalences = set(r_idx for r_idx in range(len(domain_data.state_pair_equivalences)) if r_idx not in good_equivalences)
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
