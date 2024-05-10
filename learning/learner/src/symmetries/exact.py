import logging
import time

from pathlib import Path
from collections import defaultdict, deque
from typing import Dict

from pymimir import DomainParser, ProblemParser, LiftedSuccessorGenerator, State, StateSpace
from pynauty import Graph as NautyGraph, certificate

from .state_graph import StateGraph
from ..util.command import change_dir
from .key_to_int import KeyToInt
from .logger import initialize_logger, add_console_handler
from .uvc_graph import UVCGraph


def create_pynauty_undirected_vertex_colored_graph(uvc_graph: UVCGraph) -> NautyGraph:
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

        # sprint(str(graph))

        return graph


def compute_nauty_certificate(nauty_graph: NautyGraph):
    return certificate(nauty_graph)

logger = initialize_logger("exact")

class Driver:
    def __init__(self, domain_file_path : Path, problem_file_path : Path, max_num_states : int, verbosity: str, dump_dot: bool, coloring_function: KeyToInt = None):
        self._domain_file_path = domain_file_path
        self._problem_file_path = problem_file_path
        self._max_num_states = max_num_states
        self._coloring_function = coloring_function if coloring_function is not None else KeyToInt()
        self._dump_dot = dump_dot

        global logger
        self._logger = logger
        self._logger.setLevel(verbosity)

        self._domain_parser = DomainParser(str(self._domain_file_path))
        self._domain = self._domain_parser.parse()
        self._problem_parser = ProblemParser(str(self._problem_file_path))
        self._problem = self._problem_parser.parse(self._domain)

        self._logger.info("Started generating state space")
        self._successor_generator = LiftedSuccessorGenerator(self._problem)
        self._state_space = StateSpace.new(self._problem, self._successor_generator, self._max_num_states)
        self._logger.info("Finished generating state space")


    def get_max_distance_equivalence_class_keys(self):
        equivalence_class_keys = []
        max_distance = self._state_space.get_longest_distance_to_goal_state()
        for state in self._state_space.get_states():
            goal_distance = self._state_space.get_distance_to_goal_state(state)
            if goal_distance != -1 and goal_distance == max_distance:
                state_graph = StateGraph(state, self._coloring_function)
                nauty_certificate = compute_nauty_certificate(create_pynauty_undirected_vertex_colored_graph(state_graph.uvc_graph))
                equivalence_class_key = (nauty_certificate, state_graph.uvc_graph.get_color_histogram())
                equivalence_class_keys.append(equivalence_class_key)

        return equivalence_class_keys


    def run(self):
        """ Main loop for computing Aut(S(P)) for state space S(P).
        """
        print("Domain file:", self._domain_file_path)
        print("Problem file:", self._problem_file_path)
        if self._state_space is None:
            print("Number of states is too large. Limit is:", self._max_num_states)
            return [None] * 7

        with change_dir("uvcs", enable=self._dump_dot):
            equivalence_class_key_to_class_index = dict()
            class_index_to_successor_class_indices = defaultdict(set)
            class_index_to_states = defaultdict(set)
            state_to_class_index = dict()
            class_index_to_representative_state = dict()

            self._logger.info("Started generating Aut(G)")
            start_time = time.time()

            initial_state = self._state_space.get_initial_state()
            num_generated_states = 1
            initial_state_graph = StateGraph(initial_state, self._coloring_function)
            initial_nauty_certificate = compute_nauty_certificate(create_pynauty_undirected_vertex_colored_graph(initial_state_graph.uvc_graph))
            initial_equivalence_class_key = (initial_nauty_certificate, initial_state_graph.uvc_graph.get_color_histogram())

            equivalence_class_key_to_class_index[initial_equivalence_class_key] = 0
            class_index_to_representative_state[0] = initial_state
            state_to_class_index[initial_state] = 0

            queue = deque()
            queue.append(initial_state)
            closed_list = set()
            closed_list.add(initial_state)

            while queue:
                cur_state = queue.popleft()
                cur_class_index = state_to_class_index[cur_state]

                for transition in self._state_space.get_forward_transitions(cur_state):
                    suc_state = transition.target

                    state_graph = StateGraph(suc_state, self._coloring_function)
                    nauty_certificate = compute_nauty_certificate(create_pynauty_undirected_vertex_colored_graph(state_graph.uvc_graph))
                    equivalence_class_key = (nauty_certificate, state_graph.uvc_graph.get_color_histogram())

                    # Try add new class
                    if equivalence_class_key not in equivalence_class_key_to_class_index:
                        equivalence_class_key_to_class_index[equivalence_class_key] = len(equivalence_class_key_to_class_index)

                    succ_class_index = equivalence_class_key_to_class_index[equivalence_class_key]

                    # Add first occurence during brfs as representative of equivalence class
                    if succ_class_index not in class_index_to_representative_state:
                        class_index_to_representative_state[succ_class_index] = suc_state

                    # Add all occurences to equivalence class
                    class_index_to_states[succ_class_index].add(suc_state)

                    # Add mapping from state to class index
                    state_to_class_index[suc_state] = succ_class_index

                    # Add abstract transition
                    class_index_to_successor_class_indices[cur_class_index].add(succ_class_index)

                    if suc_state not in closed_list:
                        num_generated_states += 1
                        closed_list.add(suc_state)
                        queue.append(suc_state)

                        if self._dump_dot:
                            state_graph.uvc_graph.to_dot(f"{succ_class_index}/{num_generated_states}.gc")

            print()

            end_time = time.time()
            runtime = end_time - start_time
            self._logger.info("Finished generating Aut(G)")
            print(f"Total time: {runtime:.2f} seconds")
            print("Number of generated states:", num_generated_states)
            print("Number of equivalence classes:", len(equivalence_class_key_to_class_index))
            print()

            return equivalence_class_key_to_class_index, class_index_to_representative_state, class_index_to_successor_class_indices, state_to_class_index

    @property
    def state_space(self):
        return self._state_space

    @property
    def domain(self):
        return self._domain

    @property
    def problem(self):
        return self._problem