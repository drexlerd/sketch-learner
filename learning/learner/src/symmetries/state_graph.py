from pymimir import State, Problem

from .color import Color
from .uvc_graph import UVCVertex, UVCGraph
from .key_to_int import KeyToInt

class StateGraph:
    """
    In this version, we give all vertices the same color
    and encode type information using loop edges
    """
    def __init__(self, state : State, coloring_function : KeyToInt):
        self._state = state
        self._coloring_function = coloring_function
        self._uvc_graph = self._create_undirected_vertex_colored_graph(state)

    def _create_undirected_vertex_colored_graph(self, state : State):
        problem = state.get_problem()
        graph = UVCGraph(state)

        vertex_function = KeyToInt()

        # Add vertices
        for obj in problem.objects:
            v = UVCVertex(
                id=vertex_function.get_int_from_key("o_" + obj.name),
                color=Color(self._coloring_function.get_int_from_key("t_" + obj.type.name), obj.type.name))
            graph.add_vertex(v)

        helper_id = 0

        # Add atom edges
        for atom in state.get_atoms():
            if atom.predicate.name == "=":
                continue

            v_pos_prev = None
            for pos, obj in enumerate(atom.terms):
                v_object_id = vertex_function.get_int_from_key("o_" + obj.name)

                # Add predicate node
                v_pos = UVCVertex(vertex_function.get_int_from_key(f"h_{helper_id}"), Color(self._coloring_function.get_int_from_key("p_" + atom.predicate.name + f":{pos}"), "p_" + atom.predicate.name + f":{pos}"))
                helper_id += 1
                graph.add_vertex(v_pos)

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
                v_object_id = vertex_function.get_int_from_key("o_" + obj.name)

                # Add predicate node
                if negated:
                    v_pos = UVCVertex(vertex_function.get_int_from_key(f"h_{helper_id}"), Color(self._coloring_function.get_int_from_key("not p_" + atom.predicate.name + "_g" + f":{pos}"), "not p_" + atom.predicate.name + "_g" + f":{pos}"))
                else:
                    v_pos = UVCVertex(vertex_function.get_int_from_key(f"h_{helper_id}"), Color(self._coloring_function.get_int_from_key("p_" + atom.predicate.name + "_g" + f":{pos}"), "p_" + atom.predicate.name + "_g" + f":{pos}"))
                helper_id += 1
                graph.add_vertex(v_pos)

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

    @property
    def state(self):
        return self._state

    @property
    def uvc_graph(self):
        return self._uvc_graph
