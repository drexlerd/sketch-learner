from typing import List

from .instance_data import InstanceData
from .tuple_graph_data import TupleGraphData
from .tuple_graph_minimizer import TupleGraphMinimizer
from .tuple_graph_factory import TupleGraphFactory


class TupleGraphDataFactory:
    def make_tuple_graph_datas(self,
        config,
        instance_datas: List[InstanceData]):
        tuple_graph_datas = []
        for instance_data in instance_datas:
            tuple_graph_factory = TupleGraphFactory(config.width, instance_data)
            tuple_graph_minimizer = TupleGraphMinimizer()
            tuple_graphs_by_state_index = [tuple_graph_factory.make_tuple_graph(i) for i in range(
                instance_data.transition_system.get_num_states())]
            minimized_tuple_graphs_by_state_index = [tuple_graph_minimizer.minimize(tuple_graph) for tuple_graph in tuple_graphs_by_state_index]
            print("Tuple graph minimizer:")
            print(f"Num generated subgoal tuples: {tuple_graph_minimizer.num_generated}")
            print(f"Num pruned subgoal tuples: {tuple_graph_minimizer.num_pruned}")
            tuple_graph_datas.append(TupleGraphData(tuple_graphs_by_state_index, minimized_tuple_graphs_by_state_index))
        return tuple_graph_datas
