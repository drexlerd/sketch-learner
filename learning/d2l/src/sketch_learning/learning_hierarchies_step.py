import dlplan
import logging

from typing import Dict, List, MutableSet, Tuple
from dataclasses import dataclass, field

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
        # TODO: create instance datas for each subproblem to be able to create seed features from static atoms
        # that hold in initial state of subproblem
        subproblem_instance_datas = SubproblemDataFactory().make_subproblem_instance_datas(config, subproblem_datas)
        state_pair_datas = StatePairDataFactory().make_state_pairs_from_subproblem_datas(subproblem_datas)
        subproblem_datas_by_rule.append(subproblem_datas)
        state_pair_datas_by_rule.append(state_pair_datas)
        instance_datas_by_rule.append([subproblem_data.instance_data for subproblem_data in subproblem_datas])

    solution_policies = []
    for rule in sketch.get_rules():
        print("Sketch rule:", rule.dlplan_rule.compute_repr())
        i = 0
        # TODO: iterate subproblems instead of the instance_datas
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
            dlplan_states = collect_dlplan_states(selected_subproblem_datas)
            domain_feature_data = DomainFeatureDataFactory().make_domain_feature_data(config, domain_data, dlplan_states)
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
            for general_subproblem_data in selected_subproblem_datas:
                assert policy.solves(general_subproblem_data)

            all_solved = True
            for general_subproblem in subproblem_datas:
                if not policy.solves(general_subproblem):
                    print("Policy fails to solve: ", general_subproblem.id)
                    all_solved = False
                    if general_subproblem.id > largest_unsolved_subproblem_idx:
                        largest_unsolved_subproblem_idx = general_subproblem.id
                        selected_subproblem_idxs = [general_subproblem.id]
                    else:
                        selected_subproblem_idxs.append(general_subproblem.id)
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


def collect_dlplan_states(subproblem_datas: List[SubproblemData]):
    dlplan_states = set()
    for subproblem_data in subproblem_datas:
        dlplan_states.update(set([subproblem_data.instance_data.transition_system.states_by_index[s_idx] for s_idx in subproblem_data.generated_states]))
    return list(dlplan_states)