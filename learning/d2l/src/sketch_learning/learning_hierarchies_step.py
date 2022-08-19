import dlplan
import logging

from typing import  List
from termcolor import colored

from .returncodes import ExitCode
from .asp.returncodes import ClingoExitCode
from .util.command import read_file
from .domain_data.domain_data_factory import DomainDataFactory
from .instance_data.instance_data import InstanceData
from .instance_data.instance_data_factory import InstanceDataFactory
from .instance_data.subproblem import SubproblemData
from .instance_data.subproblem_factory import SubproblemDataFactory
from .iteration_data.state_pair_data_factory import StatePairDataFactory
from .iteration_data.domain_feature_data_factory import DomainFeatureDataFactory
from .iteration_data.instance_feature_data_factory import InstanceFeatureDataFactory
from .iteration_data.state_pair_equivalence_data_factory import StatePairEquivalenceDataFactory
from .iteration_data.dlplan_policy_factory import DlplanPolicyFactory
from .iteration_data.policy import Policy
from .iteration_data.sketch import Sketch
from .asp.policy_asp_factory import PolicyASPFactory
from .util.timer import CountDownTimer


def run(config, data, rng):
    logging.info(colored(f"Initializing DomainData...", "green", "on_grey"))
    domain_data = DomainDataFactory().make_domain_data(config)
    logging.info(colored(f"..done", "green", "on_grey"))

    logging.info(colored(f"Initializing InstanceDatas...", "green", "on_grey"))
    instance_datas = InstanceDataFactory().make_instance_datas(config, domain_data)
    logging.info(colored(f"..done", "green", "on_grey"))

    logging.info(colored(f"Initializing Sketch and SubproblemDatas...", "green", "on_grey"))
    sketch = Sketch(dlplan.PolicyReader().read("\n".join(read_file(config.sketch_filename)), domain_data.syntactic_element_factory), config.width)
    subproblem_datas_by_rule = []
    for rule in sketch.get_rules():
        print("Sketch rule:", rule.dlplan_rule.compute_repr())
        subproblem_datas = SubproblemDataFactory().make_subproblems(instance_datas, rule)
        subproblem_datas_by_rule.append(subproblem_datas)
    logging.info(colored(f"..done", "green", "on_grey"))

    solution_policies = []
    for rule in sketch.get_rules():
        print("Sketch rule:", rule.dlplan_rule.compute_repr())
        i = 0
        subproblem_datas = subproblem_datas_by_rule[rule.id]
        selected_subproblem_idxs = [0]
        timer = CountDownTimer(config.timeout)
        while not timer.is_expired():
            logging.info(colored(f"Iteration: {i}", "red", "on_grey"))
            print(selected_subproblem_idxs)
            selected_subproblem_datas = [subproblem_datas[subproblem_idx] for subproblem_idx in selected_subproblem_idxs]
            print(f"Number of selected subproblems: {len(selected_subproblem_datas)}")

            logging.info(colored(f"Initializing StatePairDatas...", "blue", "on_grey"))
            selected_state_pair_datas = [StatePairDataFactory().make_state_pairs_from_subproblem_data(subproblem_datas[subproblem_idx]) for subproblem_idx in selected_subproblem_idxs]
            logging.info(colored(f"..done", "blue", "on_grey"))

            logging.info(colored(f"Initializing SubProblem InstanceDatas...", "green", "on_grey"))
            selected_instance_datas = [InstanceDataFactory().make_instance_data_from_subproblem_data(subproblem_datas[subproblem_idx]) for subproblem_idx in selected_subproblem_idxs]
            logging.info(colored(f"..done", "blue", "on_grey"))

            logging.info(colored(f"Initializing DomainFeatureData...", "blue", "on_grey"))
            dlplan_state_pairs = collect_dlplan_state_pairs(selected_subproblem_datas, selected_instance_datas)
            print("Number of dlplan state pairs:", len(dlplan_state_pairs))
            domain_feature_data = DomainFeatureDataFactory().make_domain_feature_data(config, domain_data, dlplan_state_pairs)
            logging.info(colored(f"..done", "blue", "on_grey"))

            logging.info(colored(f"Initializing InstanceFeatureDatas...", "blue", "on_grey"))
            instance_feature_datas = [InstanceFeatureDataFactory().make_instance_feature_data(selected_instance_data, domain_feature_data) for selected_instance_data in selected_instance_datas]
            logging.info(colored(f"..done", "blue", "on_grey"))

            logging.info(colored(f"Initializing StatePairEquivalenceDatas...", "blue", "on_grey"))
            rule_equivalence_data, state_pair_equivalence_datas = StatePairEquivalenceDataFactory().make_equivalence_datas(selected_state_pair_datas, domain_feature_data, instance_feature_datas)
            logging.info(colored(f"..done", "blue", "on_grey"))

            logging.info(colored(f"Initializing Logic Program...", "blue", "on_grey"))
            policy_asp_factory = PolicyASPFactory(config)
            facts = PolicyASPFactory(config).make_facts(domain_feature_data, rule_equivalence_data, state_pair_equivalence_datas, selected_subproblem_datas)
            policy_asp_factory.ground(facts)
            logging.info(colored(f"..done", "blue", "on_grey"))

            logging.info(colored(f"Solving Logic Program...", "blue", "on_grey"))
            symbols, returncode = policy_asp_factory.solve()
            logging.info(colored(f"..done", "blue", "on_grey"))

            policy_asp_factory.print_statistics()
            if returncode in [ClingoExitCode.UNSATISFIABLE]:
                print(colored("No policy exists that solves all geneneral subproblems!", "red", "on_grey"))
                solution_policies.append(None)
                break
            policy = Policy(DlplanPolicyFactory().make_dlplan_policy_from_answer_set(symbols, domain_feature_data))
            print("Learned policy:")
            print(policy.dlplan_policy.compute_repr())

            assert all([policy.solves(subproblem_data, instance_data) for subproblem_data, instance_data in zip(selected_subproblem_datas, selected_instance_datas)])

            all_solved, selected_subproblem_idxs = verify_policy(policy, subproblem_datas, selected_subproblem_idxs)
            if all_solved:
                print(colored("Policy solves all general subproblems!", "red", "on_grey"))
                solution_policies.append(policy)
                break
            i += 1

    logging.info(colored("Summary:", "green"))
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


def verify_policy(policy: Policy, subproblem_datas: List[SubproblemData], selected_subproblem_idxs: List[int]):
    all_solved = True
    for subproblem_data in subproblem_datas:
        instance_data = InstanceDataFactory().make_instance_data_from_subproblem_data(subproblem_data)
        if not policy.solves(subproblem_data, instance_data):
            all_solved = False
            if subproblem_data.id > max(selected_subproblem_idxs):
                selected_subproblem_idxs = [subproblem_data.id]
            else:
                selected_subproblem_idxs.append(subproblem_data.id)
            break
    return all_solved, selected_subproblem_idxs
