import logging

from pathlib import Path
from termcolor import colored

from learner.src.returncodes import ExitCode
from learner.src.instance_data.instance_data_utils import compute_instance_datas
from learner.src.instance_data.batch_data import BatchData
from learner.src.util.naming import compute_serialization_name


def run(config, data, rng):
    output = dict()
    if Path(config.workspace / compute_serialization_name(config.workspace, "generate_state_space")).exists():
        logging.info(colored("Output data is cached.", "blue", "on_grey"))
        return ExitCode.Success, output

    logging.info(colored("Constructing InstanceDatas...", "blue", "on_grey"))
    instance_datas, domain_data = compute_instance_datas(config)
    output["generate_state_space"] = BatchData(domain_data, instance_datas)
    logging.info(colored("..done", "blue", "on_grey"))
    return ExitCode.Success, output