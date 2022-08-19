from typing import List

from .instance_data import InstanceData
from .tuple_graph_data import TupleGraphData
from .tuple_graph_minimizer import TupleGraphMinimizer
from .tuple_graph_factory import TupleGraphFactory


class TupleGraphDataFactory:
    def __init__(self, width):
        self.width = width

    def make_tuple_graph_datas(self, instance_datas: List[InstanceData]):
        tuple_graph_factory = TupleGraphFactory(self.width)
        tuple_graph_minimizer = TupleGraphMinimizer()
        tuple_graph_datas = []
        for instance_data in instance_datas:
            tuple_graph_data = self.make_tuple_graph_data(instance_data, tuple_graph_factory, tuple_graph_minimizer)
            tuple_graph_datas.append(tuple_graph_data)
        tuple_graph_minimizer.statistics.print()
        return tuple_graph_datas

    def make_tuple_graph_data(self, instance_data: InstanceData, tuple_graph_factory: TupleGraphFactory, tuple_graph_minimizer: TupleGraphMinimizer):
        tuple_graphs_by_state_index = [tuple_graph_factory.make_tuple_graph(instance_data, i) for i in range(
            instance_data.transition_system.get_num_states())]
        minimized_tuple_graphs_by_state_index = [tuple_graph_minimizer.minimize(tuple_graph) for tuple_graph in tuple_graphs_by_state_index]
        return TupleGraphData(tuple_graphs_by_state_index, minimized_tuple_graphs_by_state_index)
