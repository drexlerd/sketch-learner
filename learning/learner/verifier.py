import logging

from pathlib import Path
from termcolor import colored
from typing import List
from collections import defaultdict

from .src.util.command import create_experiment_workspace, change_working_directory, change_dir, read_file
from .src.util.timer import Timer
from .src.util.console import add_console_handler
from .src.instance_data.instance_data import InstanceData
from .src.instance_data.instance_data_utils import compute_instance_datas
from .src.instance_data.tuple_graph_utils import compute_tuple_graphs

from .src.iteration_data.sketch import Sketch


def compute_smallest_unsolved_instance(sketch: Sketch,
                                       instance_datas: List[InstanceData],
                                       enable_goal_separating_features: bool):
    for instance_data in instance_datas:
        if not sketch.solves(instance_data, enable_goal_separating_features):
            return instance_data
    return None


def verify_sketch_for_problem_class(
    domain_filepath: Path,
    problem_filepath: Path,
    sketch_filepath: Path,
    workspace: Path,
    width: int,
    disable_closed_Q: bool = False,
    max_num_states_per_instance: int = 2000,
    max_time_per_instance: int = 10,
    enable_goal_separating_features: bool = True,
    enable_dump_files: bool = False
):
    # Setup arguments and workspace
    instance_filepaths = [problem_filepath]
    add_console_handler(logging.getLogger(), logging.INFO)
    create_experiment_workspace(workspace)
    change_working_directory(workspace)

    print(instance_filepaths)

    print("\n".join(read_file(str(sketch_filepath))))

    # Keep track of time
    timer = Timer()

    # Generate data
    with change_dir("input"):
        logging.info(colored("Constructing InstanceDatas...", "blue", "on_grey"))
        instance_datas, domain_data = compute_instance_datas(domain_filepath, instance_filepaths, disable_closed_Q, max_num_states_per_instance, max_time_per_instance, enable_dump_files)
        logging.info(colored("..done", "blue", "on_grey"))

        for s_idx in instance_datas[0].initial_s_idxs:
            print(instance_datas[0].state_space.get_states()[s_idx])

        for instance_data in instance_datas:
            instance_data.state_space = instance_data.complete_state_space

        logging.info(colored("Initializing TupleGraphs...", "blue", "on_grey"))
        compute_tuple_graphs(width, instance_datas, enable_dump_files)
        logging.info(colored("..done", "blue", "on_grey"))

    sketch = Sketch(domain_data.policy_builder.parse_policy("\n".join(read_file(str(sketch_filepath)))), width)

    # Check whether all equivalence states have same feature valuation
    for instance_data in instance_datas:
        for numerical in [n.get_element() for n in sketch.dlplan_policy.get_numericals()]:
            representative_feature_valuations = defaultdict(set)
            for state_index, representative_index in instance_data.state_index_to_representative_state_index.items():
                representative_feature_valuations[representative_index].add(numerical.evaluate(instance_data.complete_state_space.get_states()[state_index]))
                if len(representative_feature_valuations[representative_index]) > 1:
                    print(str(numerical))
                    for state_index2, representative_index2 in instance_data.state_index_to_representative_state_index.items():
                        if representative_index == representative_index2:
                            print(instance_data.complete_state_space.get_states()[state_index2])
                            print(numerical.evaluate(instance_data.complete_state_space.get_states()[state_index2]))
                    print(representative_feature_valuations[representative_index])
                assert(len(representative_feature_valuations[representative_index]) == 1)


        sketch.solves(instance_data, enable_goal_separating_features)




