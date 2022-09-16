import logging
import dlplan

from .instance_data import InstanceData


class InstanceDataFactory:
    def make_instance_datas(self, config, domain_data):
        instance_datas = []
        for instance_information in config.instance_informations:
            logging.info(f"Constructing InstanceData for filename {instance_information.instance_filename}")
            exitcode = dlplan.StateSpaceGenerator().generate_state_space(str(domain_data.domain_filename), str(instance_information.instance_filename), str(config.scorpion_dir))
            state_space = dlplan.StateSpaceReader().read(domain_data.vocabulary_info)
            goal_distance_information = state_space.compute_goal_distance_information()
            if not goal_distance_information.is_solvable() or \
                goal_distance_information.is_trivially_solvable():
                continue
            elif goal_distance_information.is_solvable():
                state_information = state_space.compute_state_information()
                instance_datas.append(InstanceData(len(instance_datas), instance_information, domain_data, state_space, goal_distance_information, state_information))
        # Sort the instances according to size and fix the indices afterwards
        instance_datas = sorted(instance_datas, key=lambda x : x.state_space.get_num_states())
        for instance_idx, instance_data in enumerate(instance_datas):
            instance_data.id = instance_idx
        return instance_datas
