import logging

from termcolor import colored

from learner.src.returncodes import ExitCode
from learner.src.instance_data.instance_data_utils import compute_instance_datas
from learner.src.instance_data.batch_data import BatchData


def run(config, data, rng):
    output = dict()
    logging.info(colored("Constructing InstanceDatas...", "blue", "on_grey"))
    instance_datas, domain_data = compute_instance_datas(config)
    output["generate_state_space"] = BatchData(domain_data, instance_datas)
    logging.info(colored("..done", "blue", "on_grey"))
    return ExitCode.Success, output