import logging

from pathlib import Path
from termcolor import colored

from learner.src.returncodes import ExitCode
from learner.src.instance_data.tuple_graph_utils import compute_tuple_graphs
from learner.src.instance_data.batch_data import BatchData
from learner.src.util.naming import compute_serialization_name


def run(config, data, rng):
    output = dict()
    if Path(config.workspace / compute_serialization_name(config.workspace, "generate_tuple_graphs")).exists():
        logging.info(colored("Output data is cached.", "blue", "on_grey"))
        return ExitCode.Success, output

    logging.info(colored("Loading data...", "blue", "on_grey"))
    serialization_data = data["generate_state_space"]
    domain_data = serialization_data.domain_data
    instance_datas = serialization_data.instance_datas
    logging.info(colored("..done", "blue", "on_grey"))

    output = dict()
    logging.info(colored("Initializing TupleGraphs...", "blue", "on_grey"))
    compute_tuple_graphs(config.width, instance_datas)
    output["generate_tuple_graphs"] = BatchData(domain_data, instance_datas)
    logging.info(colored("..done", "blue", "on_grey"))

    return ExitCode.Success, output