import logging

from pathlib import Path
from termcolor import colored
from typing import List, MutableSet

import pymimir as mm
from dlplan.policy import PolicyMinimizer

from .exit_codes import ExitCode
from .src.asp.encoding_type import EncodingType
from .src.asp.asp_factory import ASPFactory
from .src.asp.returncodes import ClingoExitCode
from .src.util.command import create_experiment_workspace, change_working_directory, write_file, change_dir
from .src.util.performance import memory_usage
from .src.util.timer import Timer
from .src.util.console import add_console_handler, print_separation_line
from .src.domain_data.domain_data import DomainData
from .src.instance_data.instance_data import InstanceData, StateFinder
from .src.instance_data.instance_data_utils import compute_instance_datas
from .src.instance_data.tuple_graph_utils import compute_tuple_graphs
from .src.iteration_data.learning_statistics import LearningStatistics
from .src.iteration_data.feature_pool_utils import compute_feature_pool
from .src.iteration_data.feature_valuations_utils import compute_per_state_feature_valuations
from .src.iteration_data.dlplan_policy_factory import D2sepDlplanPolicyFactory, ExplicitDlplanPolicyFactory
from .src.iteration_data.sketch import Sketch
from .src.iteration_data.state_pair_equivalence_utils import compute_state_pair_equivalences
from .src.iteration_data.tuple_graph_equivalence_utils import compute_tuple_graph_equivalences, minimize_tuple_graph_equivalences


def compute_smallest_unsolved_instance(
        domain_data: DomainData,
        instance_datas: List[InstanceData],
        selected_instance_datas: List[InstanceData],
        state_finder: StateFinder,
        sketch: Sketch,
        enable_goal_separating_features: bool):
    for instance_data in selected_instance_datas:
        if not sketch.solves(domain_data, instance_datas, state_finder, instance_data, enable_goal_separating_features):
            return instance_data
    return None


def learn_sketch_for_problem_class(
    domain_filepath: Path,
    problems_directory: Path,
    workspace: Path,
    width: int,
    disable_closed_Q: bool = False,
    max_num_states_per_instance: int = 2000,
    max_time_per_instance: int = 10,
    encoding_type: EncodingType = EncodingType.D2,
    max_num_rules: int = 4,
    enable_goal_separating_features: bool = True,
    disable_feature_generation: bool = True,
    concept_complexity_limit: int = 9,
    role_complexity_limit: int = 9,
    boolean_complexity_limit: int = 9,
    count_numerical_complexity_limit: int = 9,
    distance_numerical_complexity_limit: int = 9,
    feature_limit: int = 1000000,
    additional_booleans: List[str] = None,
    additional_numericals: List[str] = None,
    enable_dump_files: bool = False,
):
    # Setup arguments and workspace
    if additional_booleans is None:
        additional_booleans = []
    if additional_numericals is None:
        additional_numericals = []
    instance_filepaths = list(problems_directory.iterdir())
    add_console_handler(logging.getLogger(), logging.INFO)
    create_experiment_workspace(workspace)
    change_working_directory(workspace)

    # Keep track of time
    total_timer = Timer()
    preprocessing_timer = Timer()
    asp_timer = Timer(stopped=True)
    verification_timer = Timer(stopped=True)

    # Generate data
    with change_dir("input"):
        logging.info(colored("Constructing InstanceDatas...", "blue", "on_grey"))
        instance_datas, domain_data = compute_instance_datas(domain_filepath, instance_filepaths, disable_closed_Q, max_num_states_per_instance, max_time_per_instance, enable_dump_files)
        logging.info(colored("..done", "blue", "on_grey"))
        if instance_datas is None and domain_data is None:
            raise Exception("Failed to create InstanceData.")

        state_finder = StateFinder(domain_data, instance_datas)

        logging.info(colored("Initializing TupleGraphs...", "blue", "on_grey"))
        compute_tuple_graphs(domain_data, instance_datas, state_finder, width, enable_dump_files)
        logging.info(colored("..done", "blue", "on_grey"))

    preprocessing_timer.stop()

    # Learn sketch
    with change_dir("iterations"):
        i = 0
        with change_dir(str(i), enable=enable_dump_files):
            selected_instance_idxs = [0]
            create_experiment_workspace(workspace)
            while True:
                logging.info(colored(f"Iteration: {i}", "red", "on_grey"))

                preprocessing_timer.resume()
                selected_instance_datas : List[InstanceData] = [instance_datas[subproblem_idx] for subproblem_idx in selected_instance_idxs]
                for instance_data in selected_instance_datas:
                    write_file(f"{instance_data.idx}.dot", instance_data.dlplan_ss.to_dot(1))
                    print("     ", end="")
                    print("id:", instance_data.idx,
                          "problem_filepath:", instance_data.mimir_ss.get_pddl_parser().get_problem_filepath(),
                          "num_states:", instance_data.mimir_ss.get_num_states(),
                          "num_state_equivalences:", instance_data.gfa.get_num_states())

                logging.info(colored("Initialize global faithful abstract states...", "blue", "on_grey"))
                gfa_states : MutableSet[mm.GlobalFaithfulAbstractState] = set()
                for instance_data in selected_instance_datas:
                    gfa_states.update(instance_data.gfa.get_states())
                domain_data.gfa_states = list(gfa_states)
                logging.info(colored("..done", "blue", "on_grey"))

                logging.info(colored("Initializing DomainFeatureData...", "blue", "on_grey"))
                compute_feature_pool(
                    domain_data,
                    instance_datas,
                    selected_instance_datas,
                    state_finder,
                    disable_feature_generation,
                    concept_complexity_limit,
                    role_complexity_limit,
                    boolean_complexity_limit,
                    count_numerical_complexity_limit,
                    distance_numerical_complexity_limit,
                    feature_limit,
                    additional_booleans,
                    additional_numericals)
                logging.info(colored("..done", "blue", "on_grey"))

                logging.info(colored("Constructing PerStateFeatureValuations...", "blue", "on_grey"))
                compute_per_state_feature_valuations(domain_data, instance_datas, selected_instance_datas, state_finder)
                logging.info(colored("..done", "blue", "on_grey"))

                logging.info(colored("Constructing StatePairEquivalenceDatas...", "blue", "on_grey"))
                compute_state_pair_equivalences(domain_data, instance_datas, selected_instance_datas, state_finder)
                logging.info(colored("..done", "blue", "on_grey"))

                logging.info(colored("Constructing TupleGraphEquivalences...", "blue", "on_grey"))
                compute_tuple_graph_equivalences(domain_data, instance_datas, selected_instance_datas, state_finder)
                logging.info(colored("..done", "blue", "on_grey"))

                logging.info(colored("Minimizing TupleGraphEquivalences...", "blue", "on_grey"))
                # minimize_tuple_graph_equivalences(selected_instance_datas)
                logging.info(colored("..done", "blue", "on_grey"))
                preprocessing_timer.stop()

                asp_timer.resume()
                if encoding_type == EncodingType.D2:
                    d2_facts = set()
                    symbols = None
                    j = 0
                    while True:
                        asp_factory = ASPFactory(encoding_type, enable_goal_separating_features, max_num_rules)
                        facts = asp_factory.make_facts(domain_data, instance_datas, selected_instance_datas, state_finder)
                        #for fact in sorted(facts):
                        #    print(fact)
                        if j == 0:
                            d2_facts.update(asp_factory.make_initial_d2_facts(domain_data, instance_datas, selected_instance_datas, state_finder))
                            print("Number of initial D2 facts:", len(d2_facts))
                        elif j > 0:
                            unsatisfied_d2_facts = asp_factory.make_unsatisfied_d2_facts(domain_data, symbols)
                            d2_facts.update(unsatisfied_d2_facts)
                            print("Number of unsatisfied D2 facts:", len(unsatisfied_d2_facts))
                        print("Number of D2 facts:", len(d2_facts), "of", len(domain_data.state_pair_equivalences) ** 2)
                        facts.extend(list(d2_facts))

                        logging.info(colored("Grounding Logic Program...", "blue", "on_grey"))
                        asp_factory.ground(facts)
                        logging.info(colored("..done", "blue", "on_grey"))

                        logging.info(colored("Solving Logic Program...", "blue", "on_grey"))
                        symbols, returncode = asp_factory.solve()
                        logging.info(colored("..done", "blue", "on_grey"))

                        if returncode in [ClingoExitCode.UNSATISFIABLE, ClingoExitCode.EXHAUSTED]:
                            print(colored("ASP is unsatisfiable!", "red", "on_grey"))
                            print(colored(f"No sketch of width {width} exists that solves all instances!", "red", "on_grey"))
                            exit(ExitCode.UNSOLVABLE)
                        elif returncode == ClingoExitCode.UNKNOWN:
                            print(colored("ASP solving throws unknown error!", "red", "on_grey"))
                            exit(ExitCode.UNKNOWN)
                        elif returncode == ClingoExitCode.INTERRUPTED:
                            print(colored("ASP solving iterrupted!", "red", "on_grey"))
                            exit(ExitCode.INTERRUPTED)

                        asp_factory.print_statistics()
                        dlplan_policy = D2sepDlplanPolicyFactory().make_dlplan_policy_from_answer_set(symbols, domain_data)
                        sketch = Sketch(dlplan_policy, width)
                        logging.info("Learned the following sketch:")
                        sketch.print()
                        if compute_smallest_unsolved_instance(domain_data, instance_datas, selected_instance_datas, state_finder, sketch, enable_goal_separating_features) is None:
                            # Stop adding D2-separation constraints
                            # if sketch solves all training instances
                            break
                        j += 1
                elif encoding_type == EncodingType.EXPLICIT:
                    asp_factory = ASPFactory(encoding_type, enable_goal_separating_features, max_num_rules)
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
                    sketch = Sketch(dlplan_policy, width)
                    logging.info("Learned the following sketch:")
                    sketch.print()
                else:
                    raise RuntimeError("Unknown encoding type:", encoding_type)

                asp_timer.stop()

                verification_timer.resume()
                logging.info(colored("Verifying learned sketch...", "blue", "on_grey"))
                assert compute_smallest_unsolved_instance(domain_data, instance_datas, selected_instance_datas, state_finder, sketch, enable_goal_separating_features) is None
                smallest_unsolved_instance = compute_smallest_unsolved_instance(domain_data, instance_datas, instance_datas, state_finder, sketch, enable_goal_separating_features)
                logging.info(colored("..done", "blue", "on_grey"))
                verification_timer.stop()

                if smallest_unsolved_instance is None:
                    print(colored("Sketch solves all instances!", "red", "on_grey"))
                    break
                else:
                    if smallest_unsolved_instance.idx > max(selected_instance_idxs):
                        selected_instance_idxs = [smallest_unsolved_instance.idx]
                    else:
                        selected_instance_idxs.append(smallest_unsolved_instance.idx)
                    print("Smallest unsolved instance:", smallest_unsolved_instance.idx)
                    print("Selected instances:", selected_instance_idxs)
                i += 1

    total_timer.stop()

    # Output the result
    with change_dir("output"):
        print_separation_line()
        logging.info(colored("Summary:", "green", "on_grey"))

        learning_statistics = LearningStatistics(
            num_training_instances=len(instance_datas),
            num_selected_training_instances=len(selected_instance_datas),
            num_states_in_selected_training_instances=sum(instance_data.gfa.get_num_states() for instance_data in selected_instance_datas),
            num_states_in_complete_selected_training_instances=sum(instance_data.mimir_ss.get_num_states() for instance_data in selected_instance_datas),
            num_features_in_pool=len(domain_data.feature_pool))
        learning_statistics.print()
        print_separation_line()

        print("Resulting sketch:")
        sketch.print()
        print_separation_line()

        print("Resulting minimized sketch:")
        sketch_minimized = Sketch(PolicyMinimizer().minimize(sketch.dlplan_policy, domain_data.policy_builder), sketch.width)
        sketch_minimized.print()
        print_separation_line()

        create_experiment_workspace(workspace / "output")
        write_file(f"sketch_{width}.txt", str(sketch.dlplan_policy))
        write_file(f"sketch_minimized_{width}.txt", str(sketch_minimized.dlplan_policy))

        print_separation_line()
        print(f"Preprocessing time: {int(preprocessing_timer.get_elapsed_sec()) + 1} seconds.")
        print(f"ASP time: {int(asp_timer.get_elapsed_sec()) + 1} seconds.")
        print(f"Verification time: {int(verification_timer.get_elapsed_sec()) + 1} seconds.")
        print(f"Total time: {int(total_timer.get_elapsed_sec()) + 1} seconds.")
        print(f"Total memory: {int(memory_usage() / 1024)} GiB.")
        #print("Num states in training data before symmetry pruning:", num_states)
        #print("Num states in training data after symmetry pruning:", num_partitions)
        print_separation_line()

        print(flush=True)



