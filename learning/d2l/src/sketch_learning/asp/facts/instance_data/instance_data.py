from .transition_system import TransitionSystemFactFactory

from ....instance_data.instance_data import InstanceData


class InstanceDataFactFactory:
    def make_facts(self, instance_data: InstanceData):
        facts = []
        facts.extend(TransitionSystemFactFactory().make_facts(instance_data.id, instance_data.transition_system))
        return facts