import logging

from typing import List
from termcolor import colored


from learner.src.domain_data.domain_data_factory import DomainDataFactory
from learner.src.instance_data.instance_data import InstanceData
from learner.src.instance_data.instance_data_factory import InstanceDataFactory
from learner.src.instance_data.tuple_graph_factory import TupleGraphFactory
from learner.src.iteration_data.sketch import Sketch
from learner.src.returncodes import ExitCode
from learner.src.iteration_data.learn_sketch import learn_sketch


def run(config, data, rng):
    logging.info(colored("Initializing DomainData...", "blue", "on_grey"))
    domain_data = DomainDataFactory().make_domain_data(config)
    logging.info(colored("..done", "blue", "on_grey"))

    logging.info(colored("Initializing InstanceDatas...", "blue", "on_grey"))
    instance_datas = InstanceDataFactory().make_instance_datas(config, domain_data)
    logging.info(colored("..done", "blue", "on_grey"))

    logging.info(colored("Initializing TupleGraphs...", "blue", "on_grey"))
    tuple_graph_factory = TupleGraphFactory(config.width)
    for instance_data in instance_datas:
        instance_data.set_tuple_graphs(tuple_graph_factory.make_tuple_graphs(instance_data))
    logging.info(colored("..done", "blue", "on_grey"))

    sketch = learn_sketch(config, domain_data, instance_datas, config.workspace / "learning")

    print("Summary:")
    print("Sketch:")
    sketch.print()
    return ExitCode.Success, None
