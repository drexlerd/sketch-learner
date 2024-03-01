import logging
from termcolor import colored

from learner.src.returncodes import ExitCode
from learner.src.iteration_data.learn_sketch import learn_sketch
from learner.src.util.command import create_experiment_workspace, write_file
from learner.src.instance_data.instance_data_utils import compute_instance_datas
from learner.src.instance_data.tuple_graph_utils import compute_tuple_graphs


def run(config, data, rng):
    logging.info(colored("Constructing InstanceDatas...", "blue", "on_grey"))
    instance_datas, domain_data = compute_instance_datas(config)
    logging.info(colored("..done", "blue", "on_grey"))

    logging.info(colored("Initializing TupleGraphs...", "blue", "on_grey"))
    compute_tuple_graphs(config.width, instance_datas)
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
