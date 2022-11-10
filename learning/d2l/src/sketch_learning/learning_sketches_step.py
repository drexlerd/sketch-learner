import logging
import dlplan

from termcolor import colored
from typing import List
from sketch_learning.asp.asp_factory import ASPFactory

from sketch_learning.asp.returncodes import ClingoExitCode

from .asp.asp_factory import ASPFactory
from .domain_data.domain_data_factory import DomainDataFactory
from .instance_data.instance_data import InstanceData
from .instance_data.iteration_information import IterationInformation
from .instance_data.instance_data_factory import InstanceDataFactory
from .instance_data.tuple_graph_factory import TupleGraphFactory
from .iteration_data.domain_feature_data_factory import DomainFeatureDataFactory
from .iteration_data.feature_valuations_factory import FeatureValuationsFactory
from .iteration_data.dlplan_policy_factory import DlplanPolicyFactory
from .iteration_data.sketch import Sketch
from .iteration_data.state_pair_equivalence_factory import StatePairEquivalenceFactory
from .iteration_data.tuple_graph_equivalence_factory import TupleGraphEquivalenceFactory
from .iteration_data.tuple_graph_equivalence_minimizer import TupleGraphEquivalenceMinimizer
from .returncodes import ExitCode
from .util.timer import CountDownTimer
from .util.command import create_experiment_workspace, write_file
from .util.clock import Clock


def run(config, data, rng):
    preprocessing_clock = Clock("PREPROCESSING")
    preprocessing_clock.set_start()
    logging.info(colored(f"Initializing DomainData...", "blue", "on_grey"))
    domain_data = DomainDataFactory().make_domain_data(config)
    logging.info(colored(f"..done", "blue", "on_grey"))

    logging.info(colored(f"Initializing InstanceDatas...", "blue", "on_grey"))
    instance_datas = InstanceDataFactory().make_instance_datas(config, domain_data)
    for instance_data in instance_datas:
        instance_data.initial_s_idxs = [s_idx for s_idx in instance_data.state_space.get_state_indices() if instance_data.goal_distance_information.is_alive(s_idx)]
    logging.info(colored(f"..done", "blue", "on_grey"))

    logging.info(colored(f"Initializing TupleGraphs...", "blue", "on_grey"))
    tuple_graph_factory = TupleGraphFactory(config.output_width)
    for instance_data in instance_datas:
        instance_data.set_tuple_graphs(tuple_graph_factory.make_tuple_graphs(instance_data))
    logging.info(colored(f"..done", "blue", "on_grey"))
    preprocessing_clock.set_end()

    learning_clock = Clock("LEARNING")
    learning_clock.set_start()
    sketch, structurally_minimized_sketch = learn_sketch(config, domain_data, instance_datas, config.experiment_dir / "learning")
    learning_clock.set_end()

    print("Summary:")
    print("Resulting sketch:")
    sketch.print()
    write_file(config.experiment_dir / f"{config.domain_dir}_{config.output_width}.txt", sketch.dlplan_policy.compute_repr())
    print("Resulting structurally minimized sketch:")
    structurally_minimized_sketch.print()
    write_file(config.experiment_dir / f"{config.domain_dir}_{config.output_width}_structurally_minimized.txt", structurally_minimized_sketch.dlplan_policy.compute_repr())

    preprocessing_clock.print()
    learning_clock.print()
    return ExitCode.Success, None


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
        iteration_directory = workspace / f"iteration_{i}"
        create_experiment_workspace(iteration_directory)
        print()
        logging.info(colored(f"Iteration: {i}", "red", "on_grey"))
        selected_instance_datas = [instance_datas[subproblem_idx] for subproblem_idx in selected_instance_idxs]
        print(f"Number of selected instances: {len(selected_instance_datas)}")
        print(f"Selected instances:")
        for instance_data in selected_instance_datas:
            print("    id:", instance_data.id, "name:", instance_data.instance_information.name)
            print("initial states:", instance_data.initial_s_idxs)
            instance_data.set_iteration_information(IterationInformation(iteration_directory / instance_data.instance_information.name, instance_data.instance_information.name))

        logging.info(colored(f"Initializing DomainFeatureData...", "blue", "on_grey"))
        domain_feature_data_factory = DomainFeatureDataFactory()
        domain_feature_data = domain_feature_data_factory.make_domain_feature_data_from_instance_datas(config, domain_data, selected_instance_datas)
        domain_feature_data_factory.statistics.print()
        #for feature in domain_feature_data.numerical_features.features_by_index:
        #    print(feature.dlplan_feature.compute_repr())
        logging.info(colored(f"..done", "blue", "on_grey"))

        logging.info(colored(f"Initializing InstanceFeatureDatas...", "blue", "on_grey"))
        for instance_data in selected_instance_datas:
            instance_data.set_feature_valuations(FeatureValuationsFactory().make_feature_valuations(instance_data, domain_feature_data))
        logging.info(colored(f"..done", "blue", "on_grey"))

        logging.info(colored(f"Initializing StatePairEquivalenceDatas...", "blue", "on_grey"))
        state_pair_equivalence_factory = StatePairEquivalenceFactory()
        rule_equivalences = state_pair_equivalence_factory.make_state_pair_equivalences(domain_feature_data, selected_instance_datas)
        logging.info(colored(f"..done", "blue", "on_grey"))

        logging.info(colored(f"Initializing TupleGraphEquivalences...", "blue", "on_grey"))
        for instance_data in selected_instance_datas:
            instance_data.set_tuple_graph_equivalences(TupleGraphEquivalenceFactory().make_tuple_graph_equivalence_datas(instance_data))
        logging.info(colored(f"..done", "blue", "on_grey"))

        logging.info(colored(f"Initializing TupleGraphEquivalenceMinimizer...", "blue", "on_grey"))
        tuple_graph_equivalence_minimizer = TupleGraphEquivalenceMinimizer()
        for instance_data in selected_instance_datas:
            instance_data.set_tuple_graph_equivalences(tuple_graph_equivalence_minimizer.minimize(instance_data))
        logging.info(colored(f"..done", "blue", "on_grey"))

        # Iteratively add D2-separation constraints
        d2_facts = set()
        symbols = None
        j = 0
        while True:
            asp_factory = ASPFactory(config)
            facts = asp_factory.make_facts(domain_feature_data, rule_equivalences, selected_instance_datas)
            if j == 0:
                d2_facts.update(asp_factory.make_initial_d2_facts(selected_instance_datas))
                print("Number of initial D2 facts:", len(d2_facts))
            elif j > 0:
                unsatisfied_d2_facts = asp_factory.make_unsatisfied_d2_facts(symbols, rule_equivalences)
                d2_facts.update(unsatisfied_d2_facts)
                print("Number of unsatisfied D2 facts:", len(unsatisfied_d2_facts))
            print("Number of D2 facts:", len(d2_facts), "of", len(rule_equivalences.rules) ** 2)
            facts.extend(list(d2_facts))

            logging.info(colored(f"Grounding Logic Program...", "blue", "on_grey"))
            asp_factory.ground(facts)
            logging.info(colored(f"..done", "blue", "on_grey"))

            logging.info(colored(f"Solving Logic Program...", "blue", "on_grey"))
            symbols, returncode = asp_factory.solve()
            logging.info(colored(f"..done", "blue", "on_grey"))

            if returncode in [ClingoExitCode.UNSATISFIABLE]:
                print(colored("ASP is UNSAT", "red", "on_grey"))
                print(colored("No sketch exists that solves all geneneral subproblems!", "red", "on_grey"))
                exit(1)
            asp_factory.print_statistics()
            sketch = Sketch(DlplanPolicyFactory().make_dlplan_policy_from_answer_set(symbols, domain_feature_data, rule_equivalences), width=0)
            logging.info("Learned the following sketch:")
            sketch.print()
            if compute_smallest_unsolved_instance(config, sketch, selected_instance_datas) is None:
                # Stop adding D2-separation constraints
                # if sketch solves all training instances by luck
                break
            j += 1

        logging.info(colored(f"Verifying learned sketch...", "blue", "on_grey"))
        assert compute_smallest_unsolved_instance(config, sketch, selected_instance_datas) is None
        smallest_unsolved_instance = compute_smallest_unsolved_instance(config, sketch, instance_datas)
        logging.info(colored(f"..done", "blue", "on_grey"))

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

    logging.info(colored("Summary:", "green", "on_grey"))
    print("Number of training instances:", len(instance_datas))
    print("Number of training instances included in the ASP:", len(selected_instance_datas))
    print("Number of states included in the ASP:", sum([instance_data.state_space.get_num_states() for instance_data in selected_instance_datas]))
    print("Number of features in the pool:", len(domain_feature_data.boolean_features.features_by_index) + len(domain_feature_data.numerical_features.features_by_index))
    print("Resulting sketch:")
    sketch.print()
    print("Resulting sketch minimized:")
    sketch_minimized = Sketch(dlplan.PolicyMinimizer().minimize(sketch.dlplan_policy), sketch.width)
    sketch_minimized.print()
    return sketch, sketch_minimized