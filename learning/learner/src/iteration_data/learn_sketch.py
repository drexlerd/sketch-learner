import logging
from dlplan.policy import PolicyMinimizer

from typing import List
from termcolor import colored

from .feature_pool_utils import compute_feature_pool
from .feature_valuations_utils import compute_per_state_feature_valuations
from .dlplan_policy_factory import D2sepDlplanPolicyFactory, ExplicitDlplanPolicyFactory
from .sketch import Sketch
from .state_pair_equivalence_utils import compute_state_pair_equivalences
from .tuple_graph_equivalence_utils import compute_tuple_graph_equivalences, minimize_tuple_graph_equivalences
from .learning_statistics import LearningStatistics

from ..defaults import EncodingType
from ..asp.asp_factory import ASPFactory
from ..asp.returncodes import ClingoExitCode
from ..instance_data.instance_data import InstanceData
from ..instance_data.instance_information import InstanceInformation
from ..util.timer import CountDownTimer
from ..util.command import create_experiment_workspace



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

        selected_instance_datas : List[InstanceData] = [instance_datas[subproblem_idx] for subproblem_idx in selected_instance_idxs]
        for instance_data in selected_instance_datas:
            instance_data.instance_information = InstanceInformation(
                instance_data.instance_information.name,
                instance_data.instance_information.filename,
                workspace / f"iteration_{i}")
            instance_data.set_state_space(instance_data.state_space, True)
            print("     id:", instance_data.id, "name:", instance_data.instance_information.name)

        logging.info(colored("Initializing DomainFeatureData...", "blue", "on_grey"))
        domain_data.feature_pool = compute_feature_pool(config, domain_data, selected_instance_datas)
        logging.info(colored("..done", "blue", "on_grey"))

        logging.info(colored("Constructing PerStateFeatureValuations...", "blue", "on_grey"))
        compute_per_state_feature_valuations(selected_instance_datas)
        logging.info(colored("..done", "blue", "on_grey"))

        logging.info(colored("Constructing StatePairEquivalenceDatas...", "blue", "on_grey"))
        compute_state_pair_equivalences(domain_data, selected_instance_datas)
        logging.info(colored("..done", "blue", "on_grey"))

        logging.info(colored("Constructing TupleGraphEquivalences...", "blue", "on_grey"))
        compute_tuple_graph_equivalences(selected_instance_datas)
        logging.info(colored("..done", "blue", "on_grey"))

        logging.info(colored("Minimizing TupleGraphEquivalences...", "blue", "on_grey"))
        minimize_tuple_graph_equivalences(selected_instance_datas)
        logging.info(colored("..done", "blue", "on_grey"))

        if config.encoding_type == EncodingType.D2:
            d2_facts = set()
            symbols = None
            j = 0
            while True:
                asp_factory = ASPFactory(config)
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
                dlplan_policy = D2sepDlplanPolicyFactory().make_dlplan_policy_from_answer_set(symbols, domain_data)
                sketch = Sketch(dlplan_policy, config.width)
                logging.info("Learned the following sketch:")
                sketch.print()
                if compute_smallest_unsolved_instance(config, sketch, selected_instance_datas) is None:
                    # Stop adding D2-separation constraints
                    # if sketch solves all training instances
                    break
                j += 1
        elif config.encoding_type == EncodingType.EXPLICIT:
            asp_factory = ASPFactory(config)
            facts = asp_factory.make_facts(domain_data, selected_instance_datas)

            logging.info(colored("Grounding Logic Program...", "blue", "on_grey"))
            asp_factory.ground(facts)
            logging.info(colored("..done", "blue", "on_grey"))

            logging.info(colored("Solving Logic Program...", "blue", "on_grey"))
            symbols, returncode = asp_factory.solve()
            logging.info(colored("..done", "blue", "on_grey"))

            if returncode == ClingoExitCode.UNSATISFIABLE:
                print("UNSAT")
                return None, None, None
            asp_factory.print_statistics()

            dlplan_policy = ExplicitDlplanPolicyFactory().make_dlplan_policy_from_answer_set(symbols, domain_data)
            sketch = Sketch(dlplan_policy, config.width)
            logging.info("Learned the following sketch:")
            sketch.print()
        else:
            raise RuntimeError("Unknown encoding type:", config.encoding_type)

        logging.info(colored("Verifying learned sketch...", "blue", "on_grey"))
        assert compute_smallest_unsolved_instance(config, sketch, selected_instance_datas) is None
        smallest_unsolved_instance = compute_smallest_unsolved_instance(config, sketch, instance_datas)
        logging.info(colored("..done", "blue", "on_grey"))

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

    print()
    print()
    logging.info(colored("Summary:", "green", "on_grey"))
    print()

    learning_statistics = LearningStatistics(
        num_training_instances=len(instance_datas),
        num_selected_training_instances=len(selected_instance_datas),
        num_states_in_selected_training_instances=sum([len(instance_data.state_space.get_states()) for instance_data in selected_instance_datas]),
        num_features_in_pool=len(domain_data.feature_pool.features))
    learning_statistics.print()
    print()

    print("Resulting sketch:")
    sketch.print()
    print()

    print("Resulting minimized sketch:")
    sketch_minimized = Sketch(PolicyMinimizer().minimize(sketch.dlplan_policy, domain_data.policy_builder), sketch.width)
    sketch_minimized.print()
    print()

    return sketch, sketch_minimized, learning_statistics
