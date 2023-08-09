import logging
from termcolor import colored

from learner.src.instance_data.instance_data_factory import InstanceDataFactory
from learner.src.instance_data.tuple_graph_factory import TupleGraphFactory
from learner.src.returncodes import ExitCode
from learner.src.iteration_data.learn_sketch import learn_sketch
from learner.src.util.command import create_experiment_workspace, write_file


def run(config, data, rng):
    logging.info(colored("Initializing InstanceDatas...", "blue", "on_grey"))
    instance_datas, domain_data = InstanceDataFactory().make_instance_datas(config)
    logging.info(colored("..done", "blue", "on_grey"))

    logging.info(colored("Initializing TupleGraphs...", "blue", "on_grey"))
    tuple_graph_factory = TupleGraphFactory(config.width)
    for instance_data in instance_datas:
        instance_data.set_tuple_graphs(tuple_graph_factory.make_tuple_graphs(instance_data))
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
