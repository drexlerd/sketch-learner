""" Module description: initialize workspace and domain config, instance configs
"""

from .command import create_experiment_workspace
from ..driver import Bunch, Experiment, BENCHMARK_DIR, BASEDIR
from ..steps import generate_pipeline


def generate_experiment(expid, domain_dir, domain, **kwargs):
    """ """
    defaults = dict(
        pipeline="d2l_pipeline",

        # The overall time limit in seconds
        timeout=6*24*60*60,

        # The directory where the experiment outputs will be left
        workspace=BASEDIR / 'workspace',

        # The maximum states that we allows in each complete state space.
        max_states_per_instance=2000,

        # The location of the asp problem file
        asp_problem_location=(BASEDIR / "src/sketch_learning/asp/problem.lp"),

        sse_location=(BASEDIR / "libs" / "scorpion"),
        sse_time_limit=5,

        # Sketch settings
        tuple_graph_if_width_exceeds=False,
        max_sketch_rules=6,

        # Feature generator settings
        complexity=8,
        time_limit=3600,
        feature_limit=10000,
        num_threads_feature_generator=8,
        generate_concept_distance_numerical=False,
        debug_features=[],

        # Clingo
        clingo_arguments=["--parallel-mode=32,split"],

        quiet=False,
        random_seed=0,
    )

    parameters = {**defaults, **kwargs}  # Copy defaults, overwrite with user-specified parameters

    # root level 0 directory for experimental data
    parameters['experiment_dir'] = parameters['workspace'] / f"{expid.replace(':', '_')}_{parameters['width']}_{parameters['max_sketch_rules']}_{parameters['complexity']}"
    create_experiment_workspace(parameters["experiment_dir"], rm_if_existed=True)

    # level 1 directory for experimental data of each iteration
    parameters["iterations_dir"] = parameters["experiment_dir"] / "iterations"

    parameters["domain_filename"] = BENCHMARK_DIR / domain_dir / f"{domain}.pddl"

    parameters["sketch_file"] = parameters['experiment_dir'] / "sketch.txt"

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
