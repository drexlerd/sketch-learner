import logging

from typing import List
from termcolor import colored

from learner.src.asp.asp_factory import ASPFactory
from learner.src.asp.returncodes import ClingoExitCode


from learner.src.instance_data.instance_data import InstanceData
from learner.src.instance_data.instance_information import InstanceInformation
from learner.src.iteration_data.domain_feature_data_factory import DomainFeatureDataFactory
from learner.src.iteration_data.feature_valuations_factory import FeatureValuationsFactory
from learner.src.iteration_data.dlplan_policy_factory import D2sepDlplanPolicyFactory
from learner.src.iteration_data.sketch import Sketch
from learner.src.iteration_data.state_pair_equivalence_factory import StatePairEquivalenceFactory
from learner.src.iteration_data.tuple_graph_equivalence_factory import TupleGraphEquivalenceFactory
from learner.src.iteration_data.tuple_graph_equivalence_minimizer import TupleGraphEquivalenceMinimizer
from learner.src.util.timer import CountDownTimer
from learner.src.util.command import create_experiment_workspace



def compute_smallest_unsolved_instance(config, sketch: Sketch, instance_datas: List[InstanceData]):
    for instance_data in instance_datas:
        if not sketch.solves(config, instance_data):
            return instance_data
    return None


def learn_sketch(config, domain_data, instance_datas, workspace):
    i = 0
    selected_instance_idxs = [0]
    timer = CountDownTimer(config.timeout)
    create_experiment_workspace(workspace, rm_if_existed=True)
    while not timer.is_expired():
        logging.info(colored(f"Iteration: {i}", "red", "on_grey"))

        selected_instance_datas = [instance_datas[subproblem_idx] for subproblem_idx in selected_instance_idxs]
        for instance_data in selected_instance_datas:
            instance_data.instance_information = InstanceInformation(
                instance_data.instance_information.name,
                instance_data.instance_information.filename,
                workspace / f"iteration_{i}")
            instance_data.set_state_space(instance_data.state_space, True)
            print("     id:", instance_data.id, "name:", instance_data.instance_information.name)
    
        logging.info(colored("Initializing DomainFeatureData...", "blue", "on_grey"))
        domain_feature_data_factory = DomainFeatureDataFactory()
        domain_feature_data_factory.make_domain_feature_data_from_instance_datas(config, domain_data, selected_instance_datas)
        domain_feature_data_factory.statistics.print()
        logging.info(colored("..done", "blue", "on_grey"))

        logging.info(colored("Initializing InstanceFeatureDatas...", "blue", "on_grey"))
        for instance_data in selected_instance_datas:
            instance_data.set_feature_valuations(FeatureValuationsFactory().make_feature_valuations(instance_data))
        logging.info(colored("..done", "blue", "on_grey"))

        logging.info(colored("Initializing StatePairEquivalenceDatas...", "blue", "on_grey"))
        state_pair_equivalence_factory = StatePairEquivalenceFactory()
        state_pair_equivalence_factory.make_state_pair_equivalences(domain_data, selected_instance_datas)
        logging.info(colored("..done", "blue", "on_grey"))

        logging.info(colored("Initializing TupleGraphEquivalences...", "blue", "on_grey"))
        tuple_graph_equivalence_factory = TupleGraphEquivalenceFactory()
        tuple_graph_equivalence_factory.make_tuple_graph_equivalences(domain_data, selected_instance_datas)
        tuple_graph_equivalence_factory.statistics.print()
        logging.info(colored("..done", "blue", "on_grey"))

        # logging.info(colored(f"Initializing TupleGraphEquivalenceMinimizer...", "blue", "on_grey"))
        tuple_graph_equivalence_minimizer = TupleGraphEquivalenceMinimizer()
        for instance_data in selected_instance_datas:
            tuple_graph_equivalence_minimizer.minimize(instance_data)
        logging.info(colored("..done", "blue", "on_grey"))

        d2_facts = set()
        symbols = None
        j = 0
        while True:
            asp_factory = ASPFactory()
            asp_factory.load_problem_file(config.asp_location / config.asp_name)
            facts = asp_factory.make_facts(domain_data, selected_instance_datas)
            if j == 0:
                d2_facts.update(asp_factory.make_initial_d2_facts(selected_instance_datas))
                print("Number of initial D2 facts:", len(d2_facts))
            elif j > 0:
                unsatisfied_d2_facts = asp_factory.make_unsatisfied_d2_facts(domain_data, symbols)
                d2_facts.update(unsatisfied_d2_facts)
                print("Number of unsatisfied D2 facts:", len(unsatisfied_d2_facts))
            print("Number of D2 facts:", len(d2_facts), "of", len(domain_data.domain_state_pair_equivalence.rules) ** 2)
            facts.extend(list(d2_facts))

            logging.info(colored("Grounding Logic Program...", "blue", "on_grey"))
            asp_factory.ground(facts)
            logging.info(colored("..done", "blue", "on_grey"))

            logging.info(colored("Solving Logic Program...", "blue", "on_grey"))
            symbols, returncode = asp_factory.solve()
            logging.info(colored("..done", "blue", "on_grey"))

            if returncode in [ClingoExitCode.UNSATISFIABLE]:
                print(colored("ASP is UNSAT", "red", "on_grey"))
                print(colored("No sketch exists that solves all geneneral subproblems!", "red", "on_grey"))
                exit(1)
            asp_factory.print_statistics()
            booleans, numericals, dlplan_policy = D2sepDlplanPolicyFactory().make_dlplan_policy_from_answer_set(symbols, domain_data)
            sketch = Sketch(booleans, numericals, dlplan_policy, config.width)
            logging.info("Learned the following sketch:")
            sketch.print()
            if compute_smallest_unsolved_instance(config, sketch, selected_instance_datas) is None:
                # Stop adding D2-separation constraints
                # if sketch solves all training instances by luck
                break
            j += 1

        logging.info(colored("Verifying learned sketch...", "blue", "on_grey"))
        assert compute_smallest_unsolved_instance(config, sketch, selected_instance_datas) is None
        smallest_unsolved_instance = compute_smallest_unsolved_instance(config, sketch, instance_datas)
        logging.info(colored("..done", "blue", "on_grey"))

        logging.info(colored("Iteration summary:", "yellow", "on_grey"))
        domain_feature_data_factory.statistics.print()
        state_pair_equivalence_factory.statistics.print()
        tuple_graph_equivalence_minimizer.statistics.print()

        if smallest_unsolved_instance is None:
            print(colored("Sketch solves all instances!", "red", "on_grey"))
            break
        else:
            if smallest_unsolved_instance.id > max(selected_instance_idxs):
                selected_instance_idxs = [smallest_unsolved_instance.id]
            else:
                selected_instance_idxs.append(smallest_unsolved_instance.id)
            print("Smallest unsolved instance:", smallest_unsolved_instance.id)
            print("Selected instances:", selected_instance_idxs)
        i += 1
    return sketch