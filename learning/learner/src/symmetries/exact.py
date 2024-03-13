import logging
import time

from pathlib import Path
from collections import defaultdict, deque
from typing import Dict
from concurrent.futures import ProcessPoolExecutor, as_completed

from pymimir import DomainParser, ProblemParser, LiftedSuccessorGenerator, State, StateSpace

from .state_graph import StateGraph
from ..util.command import change_dir


class Driver:
    def __init__(self, domain_file_path : Path, problem_file_path : Path, max_num_states_per_instance : int, verbosity: str, dump_dot: bool):
        self._domain_file_path = domain_file_path
        self._problem_file_path = problem_file_path
        self._max_num_states_per_instance = max_num_states_per_instance
        self._dump_dot = dump_dot
        self.logger = logging.getLogger("exact")
        self.logger.setLevel(verbosity)

    def run(self):
        """ Main loop for computing Aut(S(P)) for state space S(P).
        """
        print("Domain file:", self._domain_file_path)
        print("Problem file:", self._problem_file_path)
        print()

        with change_dir("uvcs", enable=self._dump_dot):
            domain_parser = DomainParser(str(self._domain_file_path))
            domain = domain_parser.parse()
            problem_parser = ProblemParser(str(self._problem_file_path))
            problem = problem_parser.parse(domain)
            successor_generator = LiftedSuccessorGenerator(problem)

            self.logger.info("Started generating state space")
            state_space = StateSpace.new(problem, successor_generator, self._max_num_states_per_instance)
            self.logger.info("Finished generating state space")

            if state_space is None:
                print("Number of states is too large. Limit is:", self._max_num_states_per_instance)
                return [None] * 6

            equivalence_class_key_to_class_index = dict()
            class_index_to_successor_class_indices = defaultdict(set)
            class_index_to_states = defaultdict(set)
            state_to_class_index = dict()
            class_index_to_representative_state = dict()

            self.logger.info("Started generating Aut(G)")
            start_time = time.time()

            initial_state = state_space.get_initial_state()
            num_generated_states = 1
            initial_state_graph = StateGraph(initial_state)
            initial_equivalence_class_key = (initial_state_graph.nauty_certificate, initial_state_graph.uvc_graph.get_colors())
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

                for transition in state_space.get_forward_transitions(cur_state):
                    suc_state = transition.target

                    state_graph = StateGraph(suc_state)

                    equivalence_class_key = (state_graph.nauty_certificate, state_graph.uvc_graph.get_colors())

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

                    if self._dump_dot:
                        state_graph.uvc_graph.to_dot(f"{succ_class_index}/{num_generated_states}.gc")

                    if suc_state not in closed_list:
                        num_generated_states += 1
                        closed_list.add(suc_state)
                        queue.append(suc_state)

            print()

            end_time = time.time()
            runtime = end_time - start_time
            self.logger.info("Finished generating Aut(G)")
            print(f"Total time: {runtime:.2f} seconds")
            print("Number of generated states:", num_generated_states)
            print("Number of equivalence classes:", len(equivalence_class_key_to_class_index))
            print()

            return domain, problem, class_index_to_representative_state, class_index_to_successor_class_indices, state_to_class_index, state_space