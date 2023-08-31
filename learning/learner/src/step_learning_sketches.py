import logging
from termcolor import colored

from learner.src.returncodes import ExitCode
from learner.src.iteration_data.learn_sketch import learn_sketch
from learner.src.util.command import create_experiment_workspace, write_file


def run(config, data, rng):
    logging.info(colored("Loading data...", "blue", "on_grey"))
    serialization_data = data["generate_tuple_graphs"]
    domain_data = serialization_data.domain_data
    instance_datas = serialization_data.instance_datas
    logging.info(colored("..done", "blue", "on_grey"))

    sketch, sketch_minimized = learn_sketch(config, domain_data, instance_datas, config.workspace / "learning")
    create_experiment_workspace(config.workspace / "output")
    write_file(config.workspace / "output" / f"sketch_{config.width}.txt", str(sketch.dlplan_policy))
    write_file(config.workspace / "output" / f"sketch_minimized_{config.width}.txt", str(sketch_minimized.dlplan_policy))

    print("Summary:")
    print("Sketch:")
    sketch.print()
    print("Sketch minimized:")
    sketch_minimized.print()
    return ExitCode.Success, None
