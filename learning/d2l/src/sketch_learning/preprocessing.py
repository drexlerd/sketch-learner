from .util.timer import Timer
from .instance_data.instance_data_factory import InstanceDataFactory
from .instance_data.return_codes import ReturnCode
from .domain_data.domain_data_factory import DomainDataFactory


def preprocess_instances(config, ):
    data_preprocessing_timer = Timer(True)
    data_preprocessing_timer.resume()
    domain_data = DomainDataFactory().make_domain_data(config)
    instance_datas = []
    for instance_information in config.instance_informations:
        instance_data, return_code = InstanceDataFactory().make_instance_data(config, len(instance_datas), instance_information, domain_data)
        if return_code == ReturnCode.SOLVABLE:
            assert instance_data is not None
            instance_data.print_statistics()
            instance_datas.append(instance_data)
        elif return_code == ReturnCode.TRIVIALLY_SOLVABLE:
            print(f"Instance is trivially solvable.")
        elif return_code == ReturnCode.UNSOLVABLE:
            print(f"Instance is unsolvable.")
        elif return_code == ReturnCode.EXHAUSTED_SIZE_LIMIT:
            print(f"Instance is too large. Maximum number of allowed states is: {config.max_states_per_instance}.")
        elif return_code == ReturnCode.EXHAUSTED_TIME_LIMIT:
            print(f"Instance is too large. Time limit is: {config.sse_time_limit}")
    instance_datas = sorted(instance_datas, key=lambda x : x.transition_system.get_num_states())
    data_preprocessing_timer.stop()
    print(f"Total time spent on data preprocessing: {data_preprocessing_timer.get_elapsed_sec():02}s")
    return domain_data, instance_datas