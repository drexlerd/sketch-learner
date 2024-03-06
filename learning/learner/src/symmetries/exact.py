import sys
import time

from pathlib import Path
from collections import defaultdict, deque
from typing import Dict

from pymimir import DomainParser, ProblemParser, LiftedSuccessorGenerator, State

from .state_graph import StateGraph
from .equivalence_graph import EquivalenceGraph as XEquivalenceGraph, \
    Object as XObject, \
    Constant as XConstant, \
    Predicate as XPredicate, \
    Atom as XAtom, \
    Literal as XLiteral, \
    Domain as XDomain, \
    Problem as XProblem, \
    State as XState, \
    Action as XAction, \
    Transition as XTransition, \
    write_equivalence_graph, read_equivalence_graph
from .logger import initialize_logger, add_console_handler
from .search_node import SearchNode, CreatingInfo


class Driver:
    def __init__(self, domain_file_path : Path, problem_file_path : Path, verbosity: str, dump_dot: bool, enable_pruning: bool, dump_equivalence_graph: bool, num_threads: int):
        self._domain_file_path = domain_file_path
        self._problem_file_path = problem_file_path
        self._dump_dot = dump_dot
        self._enable_pruning = enable_pruning
        self._dump_equivalence_graph = dump_equivalence_graph
        self._num_threads = num_threads
        self._logger = initialize_logger("exact")
        self._logger.setLevel(verbosity)
        add_console_handler(self._logger)

    def run(self):
        """ Main loop for computing Aut(S(P)) for state space S(P).
        """
        print("Domain file:", self._domain_file_path)
        print("Problem file:", self._problem_file_path)
        print()

        num_generated_states = 0
        equivalence_class_to_index = dict()
        class_index_to_state = dict()
        class_index_to_successor_class_indices = defaultdict(set)
        state_to_class_index = dict()

        domain_parser = DomainParser(str(self._domain_file_path))
        domain = domain_parser.parse()
        problem_parser = ProblemParser(str(self._problem_file_path))
        problem = problem_parser.parse(domain)
        successor_generator = LiftedSuccessorGenerator(problem)

        self._logger.info("Started generating Aut(G)")
        start_time = time.time()

        initial_state = problem.create_state(problem.initial)

        initial_state_graph = StateGraph(initial_state)
        initial_equivalence_class_key = (initial_state_graph.nauty_certificate, initial_state_graph.uvc_graph.get_colors())
        equivalence_class_to_index[initial_equivalence_class_key] = 0
        class_index_to_state[0] = initial_state
        state_to_class_index[initial_state] = 0

        queue = deque()
        queue.append(initial_state)
        closed_list = set()
        closed_list.add(initial_state)
        search_nodes : Dict[State, SearchNode] = dict()
        search_nodes[initial_state] = SearchNode(creating_infos=[])
        num_generated_states += 1

        while queue:
            cur_state = queue.popleft()
            cur_class_index = state_to_class_index[cur_state]

            for applicable_action in successor_generator.get_applicable_actions(cur_state):
                suc_state = applicable_action.apply(cur_state)

                state_graph = StateGraph(suc_state)

                equivalence_class_key = (state_graph.nauty_certificate, state_graph.uvc_graph.get_colors())
                if self._enable_pruning and equivalence_class_key in equivalence_class_to_index:
                    succ_class_index = equivalence_class_to_index[equivalence_class_key]
                    class_index_to_successor_class_indices[cur_class_index].add(succ_class_index)
                    continue

                if equivalence_class_key not in equivalence_class_to_index:
                    equivalence_class_to_index[equivalence_class_key] = len(equivalence_class_to_index)

                succ_class_index = equivalence_class_to_index[equivalence_class_key]
                class_index_to_state[succ_class_index] = suc_state
                state_to_class_index[suc_state] = succ_class_index
                class_index_to_successor_class_indices[cur_class_index].add(succ_class_index)

                if self._dump_dot:
                    state_graph.uvc_graph.to_dot(f"outputs/uvcs/{succ_class_index}/{num_generated_states}.gc")

                if suc_state in closed_list:
                    # Prune if state already in closed list
                    search_nodes[suc_state].creating_infos.append(CreatingInfo(cur_state, applicable_action))
                    continue
                else:
                    num_generated_states += 1
                    search_nodes[suc_state] = SearchNode(creating_infos=[CreatingInfo(cur_state, applicable_action)])
                    closed_list.add(suc_state)
                    queue.append(suc_state)

        print()

        end_time = time.time()
        runtime = end_time - start_time
        self._logger.info("Finished generating Aut(G)")
        print(f"Total time: {runtime:.2f} seconds")
        print("Number of generated states:", num_generated_states)
        print("Number of equivalence classes:", len(equivalence_class_to_index))
        print()

        if self._dump_equivalence_graph:
            constant_map = {const : XConstant(const.name) for const in domain.constants}
            object_map = {obj: XObject(obj.name) for obj in problem.objects}
            predicate_map = {pred: XPredicate(pred.name, pred.arity) for pred in domain.predicates}
            static_predicate_map = {pred: XPredicate(pred.name, pred.arity) for pred in domain.static_predicates}
            encountered_atom_map = {atom: XAtom(predicate_map[atom.predicate], [object_map[obj] for obj in atom.terms]) for atom in problem.get_encountered_atoms()}
            static_atoms = {atom: XAtom(predicate_map[atom.predicate], [object_map[obj] for obj in atom.terms]) for atom in problem.get_static_atoms()}
            goal_literal_map = {literal: XLiteral(XAtom(predicate_map[literal.atom.predicate], [object_map[obj] for obj in literal.atom.terms]), literal.negated) for literal in problem.goal}
            state_id = 0
            state_map = dict()
            for equivalent_states in class_index_to_state.values():
                for state in equivalent_states:
                    state_map[state] = state_id
                    state_id += 1
            states = {
                state_map[state]: XState(
                    state_map[state],
                    [encountered_atom_map[atom] for atom in state.get_static_atoms()],
                    [encountered_atom_map[atom] for atom in state.get_fluent_atoms()],
                    class_id
                )
                for class_id, equivalent_states in enumerate(class_index_to_state.values())
                for state in equivalent_states
            }
            transitions = defaultdict(list)
            for equivalent_states in class_index_to_state.values():
                for state in equivalent_states:
                    target_id = state_map[state]
                    for creating_info in search_nodes[state].creating_infos:
                        source_id = state_map[creating_info.parent_state]
                        if source_id == target_id:
                            continue
                        transitions[source_id].append(XTransition(source_id, target_id, XAction(creating_info.creating_action.schema.name, [object_map[obj] for obj in creating_info.creating_action.get_arguments()])))
            goal_states = set(state_map[state] for state in closed_list if state.literals_hold(problem.goal))
            domain = XDomain(list(constant_map.values()), list(predicate_map.values()), list(static_predicate_map.values()))
            problem = XProblem(list(encountered_atom_map.values()), list(static_atoms.values()), list(goal_literal_map.values()))
            graph = XEquivalenceGraph(domain, problem, states, transitions, goal_states)
            write_equivalence_graph(graph, Path("equivalence_graph.json").absolute())
            read_equivalence_graph(Path("equivalence_graph.json").absolute())

        return domain, problem, class_index_to_state, class_index_to_successor_class_indices