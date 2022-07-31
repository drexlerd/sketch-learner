import dlplan
from .returncodes import ExitCode
from .preprocessing import preprocess_instances
from .util.command import execute, write_file, read_file, create_experiment_workspace

def run(config, data, rng):
    domain_data, instance_datas = preprocess_instances(config)
    input_sketch = dlplan.PolicyReader().read("\n".join(read_file(config.input_sketch_filename)), domain_data.syntactic_element_factory)
    return ExitCode.Success, None