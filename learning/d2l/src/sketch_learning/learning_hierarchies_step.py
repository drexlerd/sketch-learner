import dlplan
import logging

from typing import Dict, List, MutableSet, Tuple
from dataclasses import dataclass, field

from sketch_learning.instance_data.instance_data import InstanceData

from .returncodes import ExitCode
from .asp.returncodes import ClingoExitCode
from .preprocessing import preprocess_instances
from .util.command import execute, write_file, read_file, create_experiment_workspace
from .instance_data.subproblem import SubproblemData, SubproblemDataFactory
from .iteration_data.state_pair_data import StatePairDataFactory
from .iteration_data.feature_data import DomainFeatureDataFactory, InstanceFeatureDataFactory, SketchFeatureDataFactory
from .iteration_data.state_pair_equivalence_data import StatePairEquivalenceDataFactory
from .iteration_data.dlplan_policy_factory import DlplanPolicyFactory
from .iteration_data.policy import Policy
from .iteration_data.sketch import Sketch
from .asp.policy_asp_factory import PolicyASPFactory
from .util.timer import Timer, CountDownTimer

def run(config, data, rng):
    domain_data, instance_datas = preprocess_instances(config)
    sketch = Sketch(dlplan.PolicyReader().read("\n".join(read_file(config.sketch_filename)), domain_data.syntactic_element_factory), config.width)
    subproblem_datas_by_rule = []
    state_pair_datas_by_rule = []
    instance_datas_by_rule = []
    for rule in sketch.get_rules():
        print("Sketch rule:", rule.dlplan_rule.compute_repr())
        subproblem_datas = SubproblemDataFactory().make_subproblems(config, instance_datas, rule)
        subproblem_instance_datas = SubproblemDataFactory().make_subproblem_instance_datas(config, subproblem_datas)
        state_pair_datas = StatePairDataFactory().make_state_pairs_from_subproblem_datas(subproblem_datas)
        subproblem_datas_by_rule.append(subproblem_datas)
        state_pair_datas_by_rule.append(state_pair_datas)
        instance_datas_by_rule.append(subproblem_instance_datas)

    solution_policies = []
    for rule in sketch.get_rules():
        print("Sketch rule:", rule.dlplan_rule.compute_repr())
        i = 0
        subproblem_datas = subproblem_datas_by_rule[rule.id]
        instance_datas = instance_datas_by_rule[rule.id]
        state_pair_datas = state_pair_datas_by_rule[rule.id]
        selected_subproblem_idxs = [0]
        largest_unsolved_subproblem_idx = 0
        timer = CountDownTimer(config.timeout)
        while not timer.is_expired():
            print("================================================================================")
            logging.info(f"Iteration: {i}")
            print("================================================================================")
            selected_subproblem_datas = [subproblem_datas[subproblem_idx] for subproblem_idx in selected_subproblem_idxs]
            print(f"Number of selected subproblems: {len(selected_subproblem_datas)}")
            selected_state_pair_datas = [state_pair_datas[subproblem_idx] for subproblem_idx in selected_subproblem_idxs]
            selected_instance_datas = [instance_datas[subproblem_idx] for subproblem_idx in selected_subproblem_idxs]
            dlplan_state_pairs = collect_dlplan_state_pairs(selected_subproblem_datas, selected_instance_datas)
            domain_feature_data = DomainFeatureDataFactory().make_domain_feature_data(config, domain_data, dlplan_state_pairs)
            sketch_feature_data = SketchFeatureDataFactory().make_sketch_feature_data(sketch)
            sketch_feature_data.print()
            instance_feature_datas = InstanceFeatureDataFactory().make_instance_feature_datas(selected_instance_datas, domain_feature_data)
            rule_equivalence_data, state_pair_equivalence_datas = StatePairEquivalenceDataFactory().make_equivalence_data(selected_state_pair_datas, domain_feature_data, instance_feature_datas)

            policy_asp_factory = PolicyASPFactory(config)
            facts = PolicyASPFactory(config).make_facts(domain_feature_data, rule_equivalence_data, state_pair_equivalence_datas, selected_subproblem_datas)
            policy_asp_factory.ground(facts)
            symbols, returncode = policy_asp_factory.solve()
            policy_asp_factory.print_statistics()
            if returncode in [ClingoExitCode.UNSATISFIABLE]:
                print("No policy exists that solves all geneneral subproblems!")
                solution_policies.append(None)
                break
            policy = Policy(DlplanPolicyFactory().make_dlplan_policy_from_answer_set(symbols, domain_feature_data))
            print("Learned policy:")
            print(policy.dlplan_policy.compute_repr())
            assert all([policy.solves(subproblem_data, instance_data) for subproblem_data, instance_data in zip(selected_subproblem_datas, selected_instance_datas)])

            all_solved = True
            for subproblem_data, instance_data in zip(subproblem_datas, instance_datas):
                if not policy.solves(subproblem_data, instance_data):
                    print("Policy fails to solve: ", subproblem_data.id)
                    all_solved = False
                    if subproblem_data.id > largest_unsolved_subproblem_idx:
                        largest_unsolved_subproblem_idx = subproblem_data.id
                        selected_subproblem_idxs = [subproblem_data.id]
                    else:
                        selected_subproblem_idxs.append(subproblem_data.id)
                    break
            if all_solved:
                print("Policy solves all general subproblems!")
                solution_policies.append(policy)
                break
            i += 1

    print("================================================================================")
    print("Summary:")
    print("================================================================================")
    print("Input sketch:")
    print(sketch.dlplan_policy.compute_repr())
    print("Learned policies by rule:")
    for rule in sketch.get_rules():
        print("Rule", rule.id, rule.dlplan_rule.compute_repr())
        if solution_policies[rule.id] is not None:
            print(solution_policies[rule.id].dlplan_policy.compute_repr())
    return ExitCode.Success, None


def collect_dlplan_state_pairs(subproblem_datas: List[SubproblemData], instance_datas: List[InstanceData]):
    dlplan_state_pairs = set()
    for subproblem_data, instance_data in zip(subproblem_datas, instance_datas):
        dlplan_seed_state = instance_data.transition_system.states_by_index[subproblem_data.root_idx]
        dlplan_state_pairs.update(set([(dlplan_seed_state, instance_data.transition_system.states_by_index[s_idx]) for s_idx in subproblem_data.generated_states]))
    return list(dlplan_state_pairs)