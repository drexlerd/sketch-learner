""" Module description: initialize workspace and domain config, instance configs
"""

import os
from pathlib import Path

from .command import create_experiment_workspace, change_working_directory, create_sym_link
from ..driver import Bunch, Experiment, BENCHMARK_DIR, BASEDIR
from ..steps import generate_pipeline


def generate_experiment(expid, domain_dir, domain, **kwargs):
    """ """
    defaults = dict(
        pipeline="sketches_pipeline",

        # The overall time limit in seconds
        timeout=6*24*60*60,

        # The directory where the experiment outputs will be left
        workspace=BASEDIR / 'workspace',

        # The maximum states that we allows in each complete state space.
        max_states_per_instance=2000,

        # The location of the asp problem file
        asp_sketch_location=(BASEDIR / "src/sketch_learning/asp/sketch_d2l.lp"),
        asp_policy_location=(BASEDIR / "src/sketch_learning/asp/policy_d2l.lp"),

        # Feature generator settings
        concept_complexity_limit=9,
        role_complexity_limit=9,
        boolean_complexity_limit=9,
        count_numerical_complexity_limit=9,
        distance_numerical_complexity_limit=9,
        time_limit=3600,
        feature_limit=1000000,
        num_threads_feature_generator=1,

        # degree of suboptimality
        delta=1.0,
        reachable_from_init=True,

        generate_concept_distance_numerical=False,

        debug_features=[],

        # Clingo
        clingo_arguments=["--parallel-mode=32,split"],

        quiet=False,
        random_seed=0,
    )

    parameters = {**defaults, **kwargs}  # Copy defaults, overwrite with user-specified parameters

    parameters["domain_dir"] = domain_dir

    # root level 0 directory for experimental data
    parameters['experiment_dir'] = parameters['workspace'] / f"{expid.replace(':', '_')}_{parameters['width']}_{parameters['concept_complexity_limit']}_{parameters['role_complexity_limit']}_{parameters['boolean_complexity_limit']}_{parameters['count_numerical_complexity_limit']}_{parameters['distance_numerical_complexity_limit']}"
    create_experiment_workspace(parameters["experiment_dir"], rm_if_existed=False)
    change_working_directory(parameters['experiment_dir'])
    create_sym_link(BASEDIR / Path("libs/dlplan/libs/scorpion") / Path("fast-downward.py"), parameters['experiment_dir'] / "fast-downward.py", overwrite=True)

    # level 1 directory to store information of each iteration
    parameters["iterations_dir"] = parameters["experiment_dir"] / "iterations"

    parameters["domain_filename"] = BENCHMARK_DIR / domain_dir / f"{domain}.pddl"

    width = parameters["width"]
    parameters["sketch_filename"] = BASEDIR / "sketches" / domain_dir / f"{domain_dir}_{width}.txt"


    # Initialize instances
    parameters["instance_informations"] = []
    for name in parameters["instances"]:
        instance_information = dict()
        instance_information["instance_filename"] = BENCHMARK_DIR / domain_dir / f"{name}.pddl"
        instance_information["workspace"] = parameters["experiment_dir"] / "preprocessing" / name
        create_experiment_workspace(instance_information["workspace"], rm_if_existed=True)
        instance_information["state_space_filename"] = parameters["experiment_dir"] / "preprocessing" / name / "state_space.txt"
        instance_information["name"] = name
        parameters["instance_informations"].append(Bunch(instance_information))

    steps = generate_pipeline(**parameters)
    return Experiment(steps, parameters)
