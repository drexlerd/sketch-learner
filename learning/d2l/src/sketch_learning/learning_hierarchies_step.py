import dlplan
import logging
from .returncodes import ExitCode
from .preprocessing import preprocess_instances
from .util.command import execute, write_file, read_file, create_experiment_workspace
from .instance_data.general_subproblem import GeneralSubproblemFactory
from .util.timer import Timer, CountDownTimer

def run(config, data, rng):
    domain_data, instance_datas = preprocess_instances(config)
    sketch = dlplan.PolicyReader().read("\n".join(read_file(config.sketch_filename)), domain_data.syntactic_element_factory)
    print(sketch.compute_repr())

    i = 0
    instance_data = instance_datas[0]
    selected_instance_datas = []
    largest_unsolved_instance_idx = 0
    timer = CountDownTimer(config.timeout)
    while not timer.is_expired():
        logging.info(f"Iteration: {i}")
        selected_instance_datas.append(instance_data)
        for rule in sketch.get_rules():
            print(rule.compute_repr())
            general_subproblem_datas = GeneralSubproblemFactory().make_general_subproblems(selected_instance_datas, sketch, rule)
        break
    return ExitCode.Success, None