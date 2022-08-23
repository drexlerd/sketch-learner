from re import sub
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
from .instance_data.subproblem import Subproblem
from .instance_data.subproblem_factory import SubproblemFactory
from .iteration_data.state_pair_data_factory import StatePairFactory
from .iteration_data.state_pair_classifier_factory import StatePairClassifierFactory
from .iteration_data.domain_feature_data_factory import DomainFeatureDataFactory
from .iteration_data.instance_feature_data_factory import InstanceFeatureDataFactory
from .iteration_data.state_pair_equivalence_factory import StatePairEquivalenceFactory
from .iteration_data.dlplan_policy_factory import DlplanPolicyFactory
from .iteration_data.policy import Policy
from .iteration_data.sketch import Sketch
from .asp.policy_asp_factory import PolicyASPFactory
from .util.timer import CountDownTimer


def run(config, data, rng):
    logging.info(colored(f"Initializing DomainData...", "blue", "on_grey"))
    domain_data = DomainDataFactory().make_domain_data(config)
    logging.info(colored(f"..done", "blue", "on_grey"))

    logging.info(colored(f"Initializing InstanceDatas...", "blue", "on_grey"))
    instance_datas = InstanceDataFactory().make_instance_datas(config, domain_data)
    logging.info(colored(f"..done", "blue", "on_grey"))

    logging.info(colored(f"Initializing Sketch and Subproblems...", "blue", "on_grey"))
    sketch = Sketch(dlplan.PolicyReader().read("\n".join(read_file(config.sketch_filename)), domain_data.syntactic_element_factory), config.width)
    subproblems_by_rule = []
    # TODO: Instead of a subproblem we want to obtain an InstanceData + TransitionClassifier
    for rule in sketch.get_rules():
        print("Sketch rule:", rule.dlplan_rule.compute_repr())
        subproblems = SubproblemFactory().make_subproblems(instance_datas, rule)
        subproblems_by_rule.append(subproblems)
    logging.info(colored(f"..done", "blue", "on_grey"))

    solution_policies = []
    for rule in sketch.get_rules():
        print("Sketch:")
        print(sketch.dlplan_policy.compute_repr())
        print("Sketch rule:", rule.dlplan_rule.compute_repr())
        i = 0
        subproblems = subproblems_by_rule[rule.id]
        selected_subproblem_idxs = [0]
        timer = CountDownTimer(config.timeout)
        while not timer.is_expired():
            logging.info(colored(f"Iteration: {i}", "red", "on_grey"))
            selected_subproblems = [subproblems[subproblem_idx] for subproblem_idx in selected_subproblem_idxs]
            print(f"Number of selected subproblems: {len(selected_subproblems)}")
            print(f"Selected subproblem indices:", selected_subproblem_idxs)

            logging.info(colored(f"Initializing StatePairs...", "blue", "on_grey"))
            state_pair_factory = StatePairFactory()
            state_pairs_by_selected_subproblem = [state_pair_factory.make_state_pairs_from_subproblem(subproblem) for subproblem in selected_subproblems]
            logging.info(colored(f"..done", "blue", "on_grey"))

            logging.info(colored(f"Initializing SubProblem InstanceDatas...", "green", "on_grey"))
            instance_datas_by_selected_subproblem = [InstanceDataFactory().make_instance_data_from_subproblem(subproblem) for subproblem in selected_subproblems]
            # state_pairs_classifier_by_selected_subproblem = [StatePairClassifierFactory().make_state_pair_classifier_from_subproblem(subproblem) for subproblem in selected_subproblems]
            logging.info(colored(f"..done", "blue", "on_grey"))

            logging.info(colored(f"Initializing DomainFeatureData...", "blue", "on_grey"))
            domain_feature_data_factory = DomainFeatureDataFactory()
            domain_feature_data = domain_feature_data_factory.make_domain_feature_data_from_subproblems(config, domain_data, selected_subproblems, instance_datas_by_selected_subproblem)
            logging.info(colored(f"..done", "blue", "on_grey"))

            logging.info(colored(f"Initializing InstanceFeatureDatas...", "blue", "on_grey"))
            instance_feature_datas_by_selected_subproblem = [InstanceFeatureDataFactory().make_instance_feature_data(selected_instance_data, domain_feature_data) for selected_instance_data in instance_datas_by_selected_subproblem]
            logging.info(colored(f"..done", "blue", "on_grey"))

            logging.info(colored(f"Initializing StatePairEquivalenceDatas...", "blue", "on_grey"))
            state_pair_equivalence_factory = StatePairEquivalenceFactory()
            rule_equivalences, state_pair_equivalences_by_selected_subproblem = state_pair_equivalence_factory.make_state_pair_equivalences(domain_feature_data, state_pairs_by_selected_subproblem, instance_feature_datas_by_selected_subproblem)
            logging.info(colored(f"..done", "blue", "on_grey"))

            logging.info(colored(f"Initializing Logic Program...", "blue", "on_grey"))
            policy_asp_factory = PolicyASPFactory(config)
            facts = PolicyASPFactory(config).make_facts(domain_feature_data, rule_equivalences, state_pair_equivalences_by_selected_subproblem, selected_subproblems, instance_feature_datas_by_selected_subproblem)
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
            policy = Policy(DlplanPolicyFactory().make_dlplan_policy_from_answer_set_d2(symbols, domain_feature_data, rule_equivalences))
            print("Learned policy:")
            print(policy.dlplan_policy.compute_repr())

            assert all([policy.solves(subproblem_data, instance_data) for subproblem_data, instance_data in zip(selected_subproblems, instance_datas_by_selected_subproblem)])

            all_solved, selected_subproblem_idxs = verify_policy(policy, subproblems, selected_subproblem_idxs)

            logging.info(colored("Iteration summary:", "yellow", "on_grey"))
            state_pair_factory.statistics.print()
            domain_feature_data_factory.statistics.print()
            state_pair_equivalence_factory.statistics.print()

            if all_solved:
                print(colored("Policy solves all general subproblems!", "red", "on_grey"))
                solution_policies.append(policy)
                break
            i += 1

    logging.info(colored("Summary:", "yellow", "on_grey"))
    print("Input sketch:")
    print(sketch.dlplan_policy.compute_repr())
    print("Learned policies by rule:")
    for rule in sketch.get_rules():
        print("Rule", rule.id, rule.dlplan_rule.compute_repr())
        if solution_policies[rule.id] is not None:
            print(solution_policies[rule.id].dlplan_policy.compute_repr())
        else:
            print("No policy found.")
    return ExitCode.Success, None


def verify_policy(policy: Policy, subproblem_datas: List[Subproblem], selected_subproblem_idxs: List[int]):
    all_solved = True
    for subproblem_data in subproblem_datas:
        instance_data = InstanceDataFactory().make_instance_data_from_subproblem(subproblem_data)
        if not policy.solves(subproblem_data, instance_data):
            all_solved = False
            if subproblem_data.id > max(selected_subproblem_idxs):
                selected_subproblem_idxs = [subproblem_data.id]
            else:
                selected_subproblem_idxs.append(subproblem_data.id)
            break
    return all_solved, selected_subproblem_idxs
