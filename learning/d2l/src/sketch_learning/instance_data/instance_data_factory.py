import logging
import dlplan

from sketch_learning.util.command import write_file

from .instance_data import InstanceData


class InstanceDataFactory:
    def make_instance_datas(self, config, domain_data):
        instance_datas = []
        for instance_information in config.instance_informations:
            logging.info(f"Constructing InstanceData for filename {instance_information.filename}")
            exitcode = dlplan.StateSpaceGenerator().generate_state_space(str(domain_data.domain_filename), str(instance_information.filename))
            state_space = dlplan.StateSpaceReader().read(domain_data.vocabulary_info, len(instance_datas))
            if state_space.get_num_states() > config.max_states_per_instance:
                continue
            goal_distance_information = state_space.compute_goal_distance_information()
            if not goal_distance_information.is_solvable():
                # unsolvable instance
                continue
            elif set(state_space.get_state_indices()) == set(state_space.get_goal_state_indices()):
                # all states are goals
                continue
            else:
                print("Num states:", state_space.get_num_states())
                novelty_base = dlplan.NoveltyBase(len(state_space.get_instance_info_ref().get_atoms()), max(1, config.output_width))
                state_information = state_space.compute_state_information()
                instance_data = InstanceData(len(instance_datas), domain_data, dlplan.DenotationsCaches(), novelty_base, instance_information)
                instance_data.set_state_space(state_space)
                instance_data.set_goal_distance_information(goal_distance_information)
                instance_data.set_state_information(state_information)
                instance_datas.append(instance_data)
        # Sort the instances according to size and fix the indices afterwards
        instance_datas = sorted(instance_datas, key=lambda x : x.state_space.get_num_states())
        for instance_idx, instance_data in enumerate(instance_datas):
            instance_data.id = instance_idx
            instance_data.state_space.get_instance_info().set_index(instance_idx)
        return instance_datas
