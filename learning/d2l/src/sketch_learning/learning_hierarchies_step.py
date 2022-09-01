from re import sub
import dlplan
import logging

from typing import  List
from termcolor import colored

from sketch_learning.instance_data.return_codes import ReturnCode

from .returncodes import ExitCode
from .asp.returncodes import ClingoExitCode
from .util.command import read_file
from .domain_data.domain_data_factory import DomainDataFactory
from .instance_data.instance_data import InstanceData
from .instance_data.instance_data_factory import InstanceDataFactory
from .instance_data.state_pair_classifier import StatePairClassifier
from .instance_data.state_pair_classifier_factory import StatePairClassifierFactory
from .instance_data.tuple_graph_factory import TupleGraphFactory
from .instance_data.transition_system_factory import TransitionSystemFactory
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

    logging.info(colored(f"Initializing TupleGraphs...", "blue", "on_grey"))
    tuple_graphs_by_instance = [TupleGraphFactory(width=0).make_tuple_graphs(instance_data) for instance_data in instance_datas]
    logging.info(colored(f"..done", "blue", "on_grey"))

    logging.info(colored(f"Initializing Sketch...", "blue", "on_grey"))
    sketch = Sketch(dlplan.PolicyReader().read("\n".join(read_file(config.sketch_filename)), domain_data.syntactic_element_factory), config.width)
    logging.info(colored(f"..done", "blue", "on_grey"))

    solution_policies = []
    for rule in sketch.get_rules():
        print("Sketch:")
        print(sketch.dlplan_policy.compute_repr())
        print("Sketch rule:", rule.dlplan_rule.compute_repr())

        logging.info(colored(f"Initializing Subproblems...", "blue", "on_grey"))
        subproblem_instance_datas = []
        state_pair_classifiers_by_instance = []
        for instance_data, tuple_graphs in zip(instance_datas, tuple_graphs_by_instance):
            for s_idx in instance_data.transition_system.s_idx_to_dlplan_state.keys():
                subproblem_instance_data, return_code = InstanceDataFactory().make_subproblem_instance_data(len(subproblem_instance_datas), instance_data, s_idx, rule)
                if return_code == ReturnCode.UNSOLVABLE:
                    continue
                # Classify delta optimal vs not delta optimal state pairs
                state_pair_classifier = StatePairClassifierFactory(config.delta).make_state_pair_classifier(subproblem_instance_data, tuple_graphs, reachable_from_init=True)
                # Free memory by restricting transition system to relevant parts.
                subproblem_instance_data.transition_system = TransitionSystemFactory().restrict_transition_system_by_state_classifier(subproblem_instance_data.transition_system, state_pair_classifier)

                subproblem_instance_datas.append(subproblem_instance_data)
                state_pair_classifiers_by_instance.append(state_pair_classifier)
        print("Number of subproblems:", len(subproblem_instance_datas))
        logging.info(colored(f"..done", "blue", "on_grey"))

        i = 0
        selected_instance_idxs = [0]
        timer = CountDownTimer(config.timeout)
        while not timer.is_expired():
            logging.info(colored(f"Iteration: {i}", "red", "on_grey"))
            selected_instance_data = [subproblem_instance_datas[subproblem_idx] for subproblem_idx in selected_instance_idxs]
            state_pair_classifiers_by_selected_instance = [state_pair_classifiers_by_instance[subproblem_idx] for subproblem_idx in selected_instance_idxs]
            print(f"Number of selected subproblems: {len(selected_instance_data)}")
            print(f"Selected subproblem indices:", selected_instance_idxs)

            logging.info(colored(f"Initializing DomainFeatureData...", "blue", "on_grey"))
            domain_feature_data_factory = DomainFeatureDataFactory()
            domain_feature_data = domain_feature_data_factory.make_domain_feature_data_from_subproblems(config, domain_data, selected_instance_data, state_pair_classifiers_by_selected_instance)
            logging.info(colored(f"..done", "blue", "on_grey"))

            logging.info(colored(f"Initializing InstanceFeatureDatas...", "blue", "on_grey"))
            instance_feature_datas_by_selected_instance = [InstanceFeatureDataFactory().make_instance_feature_data(instance_data, domain_feature_data) for instance_data in selected_instance_data]
            logging.info(colored(f"..done", "blue", "on_grey"))

            logging.info(colored(f"Initializing StatePairEquivalenceDatas...", "blue", "on_grey"))
            state_pair_equivalence_factory = StatePairEquivalenceFactory()
            rule_equivalences, state_pair_equivalences_by_selected_instance = state_pair_equivalence_factory.make_state_pair_equivalences(domain_feature_data, state_pair_classifiers_by_selected_instance, instance_feature_datas_by_selected_instance)
            logging.info(colored(f"..done", "blue", "on_grey"))

            logging.info(colored(f"Initializing Logic Program...", "blue", "on_grey"))
            policy_asp_factory = PolicyASPFactory(config)
            facts = PolicyASPFactory(config).make_facts(domain_feature_data, rule_equivalences, selected_instance_data, state_pair_equivalences_by_selected_instance, state_pair_classifiers_by_selected_instance, instance_feature_datas_by_selected_instance)
            d2_facts = policy_asp_factory.make_initial_d2_facts(state_pair_classifiers_by_selected_instance, state_pair_equivalences_by_selected_instance)
            print("Number of initial D2 facts:", len(d2_facts))
            print("Number of D2 facts:", len(d2_facts), "of", len(rule_equivalences.rules) ** 2)
            facts.extend(list(d2_facts))
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

            # Iteratively add D2-separation constraints
            satisfiable = True
            while True:
                logging.info(colored(f"Initializing Logic Program...", "blue", "on_grey"))
                policy_asp_factory = PolicyASPFactory(config)
                facts = PolicyASPFactory(config).make_facts(domain_feature_data, rule_equivalences, selected_instance_data, state_pair_equivalences_by_selected_instance, state_pair_classifiers_by_selected_instance, instance_feature_datas_by_selected_instance)
                unsatisfied_d2_facts = policy_asp_factory.make_unsatisfied_d2_facts(symbols, rule_equivalences)
                d2_facts.update(unsatisfied_d2_facts)
                facts.extend(list(d2_facts))
                print("Number of unsatisfied D2 facts:", len(unsatisfied_d2_facts))
                print("Number of D2 facts:", len(d2_facts), "of", len(rule_equivalences.rules) ** 2)
                if not unsatisfied_d2_facts:
                    break
                policy_asp_factory.ground(facts)
                logging.info(colored(f"..done", "blue", "on_grey"))

                logging.info(colored(f"Solving Logic Program...", "blue", "on_grey"))
                symbols, returncode = policy_asp_factory.solve()
                logging.info(colored(f"..done", "blue", "on_grey"))

                if returncode in [ClingoExitCode.UNSATISFIABLE]:
                    satisfiable = False
                    break
                policy_asp_factory.print_statistics()
                policy = Policy(DlplanPolicyFactory().make_dlplan_policy_from_answer_set_d2(symbols, domain_feature_data, rule_equivalences))
                logging.info("Learned the following sketch:")
                print(sketch.dlplan_policy.str())

            if not satisfiable:
                print(colored("No policy exists that solves all geneneral subproblems!", "red", "on_grey"))
                solution_policies.append(None)
                break

            logging.info(colored(f"Verifying learned policy...", "blue", "on_grey"))
            assert all([policy.solves(instance_data, state_pair_classifier) for instance_data, state_pair_classifier in zip(selected_instance_data, state_pair_classifiers_by_selected_instance)])
            all_solved, selected_instance_idxs = verify_policy(policy, subproblem_instance_datas, state_pair_classifiers_by_instance, selected_instance_idxs)
            logging.info(colored(f"..done", "blue", "on_grey"))

            logging.info(colored("Iteration summary:", "yellow", "on_grey"))
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


def verify_policy(policy: Policy, instance_datas: List[InstanceData], state_pair_classifiers: List[StatePairClassifier], selected_instance_idxs: List[int]):
    all_solved = True
    for instance_data, state_pair_classifier in zip(instance_datas, state_pair_classifiers):
        if not policy.solves(instance_data, state_pair_classifier):
            all_solved = False
            if instance_data.id > max(selected_instance_idxs):
                selected_instance_idxs = [instance_data.id]
            else:
                selected_instance_idxs.append(instance_data.id)
            break
    return all_solved, selected_instance_idxs
