from pymimir import State, Problem
from pynauty import Graph as NautyGraph, certificate as nauty_certificate

from typing import Dict
from collections import defaultdict

from .color import Color
from .uvc_graph import UVCVertex, UVCGraph


class NameToIndexMapper:
    """
    Perfect has function to map a list of types to a color
    """
    def __init__(self):
        self._str_to_int: Dict[str, int] = {}

    def add(self, string : str):
        assert string not in self._str_to_int
        number = len(self._str_to_int)
        self._str_to_int[string] = number

    def str_to_int(self, string : str):
        assert string in self._str_to_int
        return self._str_to_int[string]

    def size(self):
        return len(self._str_to_int)


class StateGraph:
    """
    In this version, we give all vertices the same color
    and encode type information using loop edges
    """
    def __init__(self, state : State):
        self._state = state

        self._uvc_graph = self._create_undirected_vertex_colored_graph(state)
        self._nauty_graph = self._create_pynauty_undirected_vertex_colored_graph(self._uvc_graph)
        self._nauty_certificate = nauty_certificate(self._nauty_graph)


    def _create_index_mapper(self, state: State):
        problem: Problem = state.get_problem()
        index_mapper = NameToIndexMapper()
        index_mapper.add(None)  # used to represent "uncolored"
        for obj in problem.objects:
            index_mapper.add("o_" + obj.name)
        for typ in problem.domain.types:
            index_mapper.add("t_" + typ.name)
        for pred in problem.domain.predicates:
            for i in range(pred.arity):
                index_mapper.add("p_" + pred.name + f":{i}")
            for i in range(pred.arity):
                index_mapper.add("p_" + pred.name + "_g" + f":{i}")
            for i in range(pred.arity):
                index_mapper.add("not p_" + pred.name + "_g" + f":{i}")
        return index_mapper

    def _create_undirected_vertex_colored_graph(self, state : State):
        problem = state.get_problem()
        graph = UVCGraph(state)

        index_mapper = self._create_index_mapper(state)
        add_vertex_id = index_mapper.size()

        # Add vertices
        for obj in problem.objects:
            v = UVCVertex(
                id=index_mapper.str_to_int("o_" + obj.name),
                color=Color(
                    value=index_mapper.str_to_int("t_" + obj.type.name),
                    info=obj.type.name))
            graph.add_vertex(v)

        # Add atom edges
        for atom in state.get_atoms():
            if atom.predicate.name == "=":
                continue

            v_pos_prev = None
            for pos, obj in enumerate(atom.terms):
                v_object_id = index_mapper.str_to_int("o_" + obj.name)

                # Add predicate node
                v_pos = UVCVertex(add_vertex_id, Color(index_mapper.str_to_int("p_" + atom.predicate.name + f":{pos}"), "p_" + atom.predicate.name + f":{pos}"))
                graph.add_vertex(v_pos)
                add_vertex_id += 1

                # Connect predicate node to object node
                graph.add_edge(v_object_id, v_pos.id)
                graph.add_edge(v_pos.id, v_object_id)

                if (v_pos_prev is not None):
                    # connect with previous positional node
                    graph.add_edge(v_pos_prev.id, v_pos.id)
                    graph.add_edge(v_pos.id, v_pos_prev.id)
                v_pos_prev = v_pos

        # Add goal literals
        for goal_literal in problem.goal:
            atom = goal_literal.atom
            negated = goal_literal.negated

            v_pos_prev = None
            for pos, obj in enumerate(atom.terms):
                v_object_id = index_mapper.str_to_int("o_" + obj.name)

                # Add predicate node
                if negated:
                    v_pos = UVCVertex(add_vertex_id, Color(index_mapper.str_to_int("not p_" + atom.predicate.name + "_g" + f":{pos}"), "not p_" + atom.predicate.name + "_g" + f":{pos}"))
                else:
                    v_pos = UVCVertex(add_vertex_id, Color(index_mapper.str_to_int("p_" + atom.predicate.name + "_g" + f":{pos}"), "p_" + atom.predicate.name + "_g" + f":{pos}"))
                graph.add_vertex(v_pos)
                add_vertex_id += 1

                # Connect predicate node to object node
                graph.add_edge(v_object_id, v_pos.id)
                graph.add_edge(v_pos.id, v_object_id)

                if v_pos_prev is not None:
                    # connect with previous positional node
                    graph.add_edge(v_pos_prev.id, v_pos.id)
                    graph.add_edge(v_pos.id, v_pos_prev.id)
                v_pos_prev = v_pos

        assert graph.test_is_undirected()
        return graph

    def _create_pynauty_undirected_vertex_colored_graph(self, uvc_graph: UVCGraph):
        # remap vertex indices
        old_to_new_vertex_index = dict()
        for vertex in uvc_graph.vertices.values():
            old_to_new_vertex_index[vertex.id] = len(old_to_new_vertex_index)
        adjacency_dict = defaultdict(set)
        for source_id, target_ids in uvc_graph.adj_list.items():
            adjacency_dict[old_to_new_vertex_index[source_id]] = set(old_to_new_vertex_index[target_id] for target_id in target_ids)
        # compute vertex partitioning
        color_to_vertices = defaultdict(set)
        for vertex in uvc_graph.vertices.values():
            color_to_vertices[vertex.color.value].add(old_to_new_vertex_index[vertex.id])
        color_to_vertices = dict(sorted(color_to_vertices.items()))
        vertex_coloring = list(color_to_vertices.values())

        graph = NautyGraph(
            number_of_vertices=len(old_to_new_vertex_index),
            directed=False,
            adjacency_dict=adjacency_dict,
            vertex_coloring=vertex_coloring)
        return graph


    @property
    def state(self):
        return self._state

    @property
    def uvc_graph(self):
        return self._uvc_graph

    @property
    def nauty_certificate(self):
        return self._nauty_certificate
