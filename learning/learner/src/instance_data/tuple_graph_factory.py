import dlplan

from learner.src.instance_data.instance_data import InstanceData


class TupleGraphFactory:
    def __init__(self, width: int):
        self.width = width

    def make_tuple_graphs(self, instance_data: InstanceData):
        tuple_graphs = dict()
        novelty_base = dlplan.NoveltyBase(len(instance_data.state_space.get_instance_info().get_atoms()), max(1, self.width))
        for s_idx in instance_data.state_space.get_states().keys():
            if instance_data.is_deadend(s_idx):
                continue
            tuple_graphs[s_idx] = dlplan.TupleGraph(novelty_base, instance_data.state_space, s_idx, self.width)
        return tuple_graphs
