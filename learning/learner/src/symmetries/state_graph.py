from pymimir import State, Problem

from typing import List, MutableSet
from collections import defaultdict

from .color import Color
from .uvc_graph import UVCVertex, UVCGraph
from .key_to_int import KeyToInt


class StateGraph:
    """
    In this version, we give all vertices the same color
    and encode type information using loop edges
    """
    def __init__(self, state : State, coloring_function: KeyToInt, mark_true_goal_atoms : bool = False):
        self._state = state
        self._coloring_function = coloring_function
        self._mark_true_goal_atoms = mark_true_goal_atoms
        self._uvc_graph = self._create_undirected_vertex_colored_graph(state)

    @staticmethod
    def get_num_vertices(state: State):
        """ Return the number of vertices in the graph.
        """
        num_vertices = len(state.get_problem().objects)
        for atom in state.get_atoms():
            arity = len(atom.terms)
            num_vertices += arity
        for goal_literal in state.get_problem().goal:
            atom = goal_literal.atom
            arity = len(atom.terms)
            num_vertices += arity
        return num_vertices


    def _create_undirected_vertex_colored_graph(self, state : State):
        problem = state.get_problem()
        graph = UVCGraph(state)

        vertex_function = KeyToInt()

        # Add vertices
        for obj in problem.objects:
            v = UVCVertex(
                id=vertex_function.get_int_from_key("o_" + obj.name),
                color=Color(
                    value=self._coloring_function.get_int_from_key("t_" + obj.type.name),
                    info=obj.type.name))
            graph.add_vertex(v)

        def translate_atom_to_atom_repr(atom):
            return (atom.predicate.name, tuple([obj.name for obj in atom.terms]))

        def translate_literal_to_atom_repr(literal):
            return (literal.atom.predicate.name, tuple([obj.name for obj in literal.atom.terms]))

        state_atoms_reprs = set(translate_atom_to_atom_repr(atom) for atom in state.get_atoms())
        goal_atoms_reprs = set(translate_literal_to_atom_repr(literal) for literal in problem.goal if not literal.negated)

        add_vertex_id = len(graph.vertices)

        # Add atom edges
        for atom in state.get_atoms():
            v_pos_prev = None
            for pos, obj in enumerate(atom.terms):
                v_object_id = vertex_function.get_int_from_key("o_" + obj.name)

                # Add predicate node
                v_pos = UVCVertex(add_vertex_id, Color(self._coloring_function.get_int_from_key("p_" + atom.predicate.name + f":{pos}"), "p_" + atom.predicate.name + f":{pos}"))
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

            if self._mark_true_goal_atoms:
                if negated:
                    if translate_literal_to_atom_repr(goal_literal) not in state_atoms_reprs:
                        suffix = "_true"
                    else:
                        suffix = "_false"
                else:
                    if translate_literal_to_atom_repr(goal_literal) in state_atoms_reprs:
                        suffix = "_true"
                    else:
                        suffix = "_false"
            else:
                suffix = ""

            v_pos_prev = None
            for pos, obj in enumerate(atom.terms):
                v_object_id = vertex_function.get_int_from_key("o_" + obj.name)

                # Add predicate node
                if negated:
                    v_pos = UVCVertex(add_vertex_id, Color(self._coloring_function.get_int_from_key("not p_" + atom.predicate.name + "_g" + suffix + f":{pos}"), "not p_" + atom.predicate.name + "_g" + suffix + f":{pos}"))
                else:
                    v_pos = UVCVertex(add_vertex_id, Color(self._coloring_function.get_int_from_key("p_" + atom.predicate.name + "_g" + suffix + f":{pos}"), "p_" + atom.predicate.name + "_g" + suffix + f":{pos}"))
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
        assert len(graph.vertices) == StateGraph.get_num_vertices(self.state)
        return graph


    @property
    def state(self):
        return self._state

    @property
    def uvc_graph(self):
        return self._uvc_graph
