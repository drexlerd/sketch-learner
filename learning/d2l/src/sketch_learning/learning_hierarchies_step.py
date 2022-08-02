import dlplan
from .returncodes import ExitCode
from .preprocessing import preprocess_instances
from .util.command import execute, write_file, read_file, create_experiment_workspace
from .instance_data.general_subproblem import GeneralSubproblemFactory


def run(config, data, rng):
    domain_data, instance_datas = preprocess_instances(config)
    sketch = dlplan.PolicyReader().read("\n".join(read_file(config.sketch_filename)), domain_data.syntactic_element_factory)
    print(sketch.compute_repr())
    for rule in sketch.get_rules():
        print(rule.compute_repr())
        GeneralSubproblemFactory().make_generalized_subproblems(instance_datas[0], sketch, rule)
    return ExitCode.Success, None