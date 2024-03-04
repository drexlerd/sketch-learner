""" Module description: initialize workspace and domain config, instance configs
"""

from pathlib import Path
from typing import List
from enum import Enum

from .util.command import create_experiment_workspace, change_working_directory
from .driver import Experiment
from .steps import generate_pipeline
from .instance_data.instance_information import InstanceInformation


class EncodingType(Enum):
    """
    D2 is the encoding related to Francès et al. (AAAI2021): https://arxiv.org/abs/2101.00692
    EXPLICIT is the encoding from Drexler et al. (ICAPS2022): https://arxiv.org/abs/2203.14852
    """
    D2 = 0
    EXPLICIT = 1


def generate_experiment(domain_filename: str, instance_filenames: List[str], workspace: str, **kwargs):
    """ """
    defaults = dict(
        ## The overall time limit in seconds
        timeout=6*24*60*60,


        ## State space generation

        # The maximum states that we allows in each complete state space
        max_states_per_instance=1000,
        # The maximum time to expand a complete state space
        max_time_per_instance=10,


        ## Feature generation

        # If true, enable feature generation
        generate_features=True,

        # The setting that are passed to DLPlan
        concept_complexity_limit=9,
        role_complexity_limit=9,
        boolean_complexity_limit=9,
        count_numerical_complexity_limit=9,
        distance_numerical_complexity_limit=9,
        time_limit=3600,
        feature_limit=1000000,

        # The features that will be added regardless of the feature generation
        # Useful for debugging or manually crafting new sketches
        add_boolean_features=[],
        add_numerical_features=[],


        ## If true, features separate goal from nongoal states
        goal_separation=False,


        ## If true, all alive states are considered initial state
        closed_Q=True,


        ## The bound on the sketch width on the training instances
        width=1,


        ## Encoding type
        encoding_type=EncodingType.D2,

        # D2 encoding settings (there are none yet)

        # Explicit encoding settings
        max_num_rules=4,


        ## Misc
        quiet=False,
        random_seed=0,
    )
    parameters = {**defaults, **kwargs}  # Copy defaults, overwrite with user-specified parameters

    workspace = Path(workspace).resolve()
    parameters["workspace"] = workspace
    parameters["domain_filename"] = domain_filename

    # root level 0 directory for experimental data
    create_experiment_workspace(workspace, rm_if_existed=False)
    change_working_directory(workspace)

    # level 1 directory to store information of each iteration
    parameters["iterations_dir"] = workspace / "iterations"

    # Initialize instances
    parameters["instance_informations"] = []
    for instance_filename in instance_filenames:
        instance_filename = Path(instance_filename)
        parameters["instance_informations"].append(
            InstanceInformation(
                instance_filename.stem,
                instance_filename,
                workspace / "input" / instance_filename.stem))

    steps, config = generate_pipeline(**parameters)

    return Experiment(steps, parameters)
