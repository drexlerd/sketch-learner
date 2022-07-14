from operator import eq
import sys
import os
import shutil
import logging
import dlplan

from collections import defaultdict
from pathlib import Path

from .returncodes import ExitCode
from .util.command import execute, write_file, read_file, create_experiment_workspace
from .util.timer import Timer, CountDownTimer

from .instance_data.instance_data import InstanceDataFactory, InstanceData
from .instance_data.return_codes import ReturnCode
from .domain_data.domain_data import DomainDataFactory, DomainData
from .iteration_data.iteration_data import IterationData
from .iteration_data.feature_data import FeatureDataFactory, FeatureData
from .iteration_data.sketch_factory import SketchFactory
from .iteration_data.equivalence_data import EquivalenceDataFactory
from .asp.fact_factory import ASPFactFactory
from .asp.answer_set_parser import AnswerSetParser, AnswerSetParser_ExitCode



def run(config, data, rng):
    data_preprocessing_timer = Timer(True)
    data_preprocessing_timer.resume()
    domain_data = DomainDataFactory().make_domain_data(config)
    instance_datas = []
    for instance_information in config.instance_informations:
        instance_data, return_code = InstanceDataFactory().make_instance_data(config, instance_information, domain_data)
        if return_code == ReturnCode.SOLVABLE:
            assert instance_data is not None
            instance_data.print_statistics()
            instance_datas.append(instance_data)
        elif return_code == ReturnCode.TRIVIALLY_SOLVABLE:
            print(f"Instance is trivially solvable.")
        elif return_code == ReturnCode.UNSOLVABLE:
            print(f"Instance is unsolvable.")
        elif return_code == ReturnCode.EXHAUSTED_SIZE_LIMIT:
            print(f"Instance is too large. Maximum number of allowed states is: {config.max_states_per_instance}.")
        elif return_code == ReturnCode.EXHAUSTED_TIME_LIMIT:
            print(f"Instance is too large. Time limit is: {config.sse_time_limit}")
    instance_datas = sorted(instance_datas, key=lambda x : x.transition_system.get_num_states())
    data_preprocessing_timer.stop()

    # Iteration index
    i = 0
    # Choose the first instance
    instance_data = instance_datas[0]
    selected_instance_datas = []
    largest_unsolved_instance_idx = 0
    asp_construction_timer = Timer(True)
    learning_timer = Timer(True)
    validation_timer = Timer(True)
    timer = CountDownTimer(config.timeout)
    while not timer.is_expired():
        logging.info(f"Iteration: {i}")
        # 1.0: Initialize iteration directory
        iteration_data = initialize_iteration_data(config, i)
        asp_construction_timer.resume()
        selected_instance_datas.append(instance_data)

        print(f"Number of selected instances: {len(selected_instance_datas)}")
        print("\n".join([str(selected_instance.instance_filename) for selected_instance in selected_instance_datas]))

        # 1.2. Generate feature pool
        feature_data = FeatureDataFactory().generate_feature_data(config, domain_data, selected_instance_datas)
        equivalence_data = EquivalenceDataFactory().make_equivalence_class_data(selected_instance_datas, feature_data)
        # 1.3. Generate asp facts
        facts = ASPFactFactory().make_asp_facts(selected_instance_datas, feature_data, equivalence_data)
        write_file(iteration_data.facts_file, facts)
        asp_construction_timer.stop()

        # 1.5. Learn the sketch
        learning_timer.resume()
        execute(["clingo", iteration_data.facts_file, config.asp_problem_location, "-c", f"max_sketch_rules={config.max_sketch_rules}"] + config.clingo_arguments, stdout=iteration_data.answer_set_file)
        learning_timer.stop()

        # 1.6. Parse the sketch from the answer set
        answer_set_file_content = read_file(iteration_data.answer_set_file)
        answer_set_datas, exitcode = AnswerSetParser().parse(answer_set_file_content)
        if exitcode == AnswerSetParser_ExitCode.Unsatisfiable:
            logging.info("UNSATISFIABLE! No sketch was found.")
            return ExitCode.Unsatisfiable, None

        sketch = SketchFactory().make_sketch(answer_set_datas[-1], feature_data, config.width)
        logging.info("Learned the following sketch:")
        print(sketch.policy.str())
        with open(iteration_data.sketch_file, "w") as file:
            file.write(dlplan.PolicyWriter().write(sketch.policy))

        # Step 2: try the sketch on all instances until there are
        # (1) either no more instances then we return the sketch, or
        # (2) the sketch fails then we add the instance and do another iteration.
        validation_timer.resume()
        all_solved = True
        assert all([sketch.solves(instance_data) for instance_data in selected_instance_datas])
        for j in range(len(instance_datas)):
            instance_data = instance_datas[j]
            if not sketch.solves(instance_data):
                all_solved = False
                if j > largest_unsolved_instance_idx:
                    largest_unsolved_instance_idx = j
                    selected_instance_datas = []
                break
        validation_timer.stop()
        if all_solved:
            break
        i += 1
        # exit(1)

    print("Incremental search statistics:")
    print(f"Number of training instances: {len(instance_datas)}")
    print(f"Number of training instances included in the ASP: {len(selected_instance_datas)}")
    print(f"Number of states included in the ASP: {sum([len(instance_data.transition_system.states_by_index) for instance_data in selected_instance_datas])}")
    print(f"Number of features in the pool: {len(feature_data.boolean_features) + len(feature_data.numerical_features)}")
    print(f"Numer of rules in policy sketch: {len(sketch.policy.get_rules())}")
    print(f"Number of features selected by policy sketch: {len(sketch.policy.get_boolean_features()) + len(sketch.policy.get_numerical_features())}")
    print(f"Maximum feature complexity of selected feature: {max([0] + [boolean_feature.get_boolean().compute_complexity() for boolean_feature in sketch.policy.get_boolean_features()] + [numerical_feature.get_numerical().compute_complexity() for numerical_feature in sketch.policy.get_numerical_features()])}")
    print(f"Total time spent on data preprocessing: {data_preprocessing_timer.get_elapsed_sec():02}s")
    print(f"Total time spent on constructing ASP facts: {asp_construction_timer.get_elapsed_sec():02}")
    print(f"Total time spent on grounding and solving ASP: {learning_timer.get_elapsed_sec():02}s")
    print(f"Total time spent on validation: {validation_timer.get_elapsed_sec():02}s")
    print("Resulting sketch:")
    print(sketch.policy.str())
    with open(config.sketch_file, "w") as file:
            file.write(dlplan.PolicyWriter().write(sketch.policy))

    return ExitCode.Success, None


def initialize_iteration_data(config, i):
    iteration_dir = config["iterations_dir"] / str(i)
    create_experiment_workspace(iteration_dir, rm_if_existed=True)

    iteration_data = IterationData()
    iteration_data.iteration_dir = iteration_dir
    iteration_data.facts_file = iteration_dir / "facts.lp"
    iteration_data.answer_set_file = iteration_dir / "answer_set.txt"
    iteration_data.sketch_file = iteration_dir / "sketch.txt"
    return iteration_data
