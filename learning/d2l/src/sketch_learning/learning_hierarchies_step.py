from .returncodes import ExitCode
from .preprocessing import preprocess_instances


def run(config, data, rng):
    domain_data, instance_datas = preprocess_instances(config)

    timer = CountDownTimer(config.timeout)
    while not timer.is_expired():
        pass
    return ExitCode.Success, None