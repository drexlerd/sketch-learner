""" Module description: initialize workspace and domain config, instance configs
"""

import os
from pathlib import Path
from typing import List

from learner.src.util.command import create_experiment_workspace, change_working_directory, create_sym_link

from learner.src.driver import Experiment, BASEDIR
from learner.src.steps import generate_pipeline
from learner.src.instance_data.instance_information import InstanceInformation


def generate_experiment(domain_filename: str, instance_filenames: List[str], workspace: str, **kwargs):
    """ """
    defaults = dict(
        # The overall time limit in seconds
        timeout=6*24*60*60,

        # The maximum states that we allows in each complete state space.
        max_states_per_instance=2000,

        # Feature generator settings
        concept_complexity_limit=9,
        role_complexity_limit=9,
        boolean_complexity_limit=9,
        count_numerical_complexity_limit=9,
        distance_numerical_complexity_limit=9,
        time_limit=3600,
        feature_limit=1000000,

        width=2,

        asp_name="sketch.lp",

        add_features=[],
        generate_features=True,

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

    # The location of the asp problem file
    config["asp_location"] = BASEDIR / "learner/src/asp/"

    return Experiment(steps, parameters)
