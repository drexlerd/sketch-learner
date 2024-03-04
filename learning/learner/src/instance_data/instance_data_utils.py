import logging
import os

from typing import  List, Tuple
from pathlib import Path

from dlplan.core import DenotationsCaches
from dlplan.state_space import GeneratorExitCode, generate_state_space

from .instance_data import InstanceData
from .instance_information import InstanceInformation

from ..domain_data.domain_data import DomainData
from ..domain_data.domain_data_utils import compute_domain_data
from ..util.command import create_experiment_workspace


def compute_instance_datas(domain_filepath: Path,
                           instance_informations: List[InstanceInformation],
                           closed_Q: bool,
                           max_num_states_per_instance: int,
                           max_time_per_instance: int) -> Tuple[List[InstanceData], DomainData]:
    cwd = os.getcwd()
    vocabulary_info = None
    instance_datas = []
    for instance_information in instance_informations:
        logging.info("Constructing InstanceData for filename %s", instance_information.filename)
        create_experiment_workspace(instance_information.workspace)
        # change working directory to put planner output files in correct directory
        os.chdir(instance_information.workspace)
        print(instance_information.workspace)
        result = generate_state_space(str(domain_filepath), str(instance_information.filename), vocabulary_info, len(instance_datas), max_time_per_instance)
        if result.exit_code != GeneratorExitCode.COMPLETE:
            continue
        state_space = result.state_space
        if vocabulary_info is None:
            # We obtain the parsed vocabulary from the first instance
            vocabulary_info = state_space.get_instance_info().get_vocabulary_info()
            domain_data = compute_domain_data(domain_filepath, vocabulary_info)
        if len(state_space.get_states()) > max_num_states_per_instance:
            continue
        goal_distances = state_space.compute_goal_distances()
        if goal_distances.get(state_space.get_initial_state_index(), None) is None:
            print("Unsolvable.")
            continue
        if set(state_space.get_states().keys()) == set(state_space.get_goal_state_indices()):
            print("Trivially solvable.")
            continue
        if not closed_Q and state_space.get_initial_state_index() in set(state_space.get_goal_state_indices()):
            print("Initial state is goal.")
            continue
        print("Num states:", len(state_space.get_states()))
        instance_data = InstanceData(len(instance_datas), domain_data, DenotationsCaches(), instance_information)
        instance_data.set_state_space(state_space, create_dump=True)
        instance_data.goal_distances = goal_distances
        if closed_Q:
            instance_data.initial_s_idxs = [s_idx for s_idx in state_space.get_states().keys() if instance_data.is_alive(s_idx)]
        else:
            instance_data.initial_s_idxs = [state_space.get_initial_state_index(),]
        print("initial state indices:", instance_data.initial_s_idxs)
        instance_datas.append(instance_data)
    # Sort the instances according to size and fix the indices afterwards
    instance_datas = sorted(instance_datas, key=lambda x : len(x.state_space.get_states()))
    for instance_idx, instance_data in enumerate(instance_datas):
        instance_data.id = instance_idx
    # change back working directory
    os.chdir(cwd)
    return instance_datas, domain_data
