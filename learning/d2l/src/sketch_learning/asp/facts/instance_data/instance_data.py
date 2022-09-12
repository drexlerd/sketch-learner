from clingo import Number

from ....instance_data.instance_data import InstanceData


class InstanceDataFactFactory:
    def make_facts(self, instance_data: InstanceData):
        facts = []
        instance_idx = instance_data.id
        for dlplan_state in instance_data.state_space.get_states_ref():
            s_idx = dlplan_state.get_index()
            if not instance_data.state_space.is_deadend(s_idx):
                facts.append(("solvable", [Number(instance_idx), Number(s_idx)]))
            if instance_data.state_space.is_goal(s_idx):
                facts.append(("goal", [Number(instance_idx), Number(s_idx)]))
            else:
                facts.append(("nongoal", [Number(instance_idx), Number(s_idx)]))
            if instance_data.state_space.is_alive(s_idx):
                facts.append(("alive", [Number(instance_idx), Number(s_idx)]))
        return list(facts)