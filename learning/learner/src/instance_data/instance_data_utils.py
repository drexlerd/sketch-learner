import logging
from typing import  List, Tuple, Dict
from pathlib import Path
from collections import defaultdict

from dlplan.core import VocabularyInfo, InstanceInfo, State, DenotationsCaches
from dlplan.state_space import StateSpace, GeneratorExitCode, generate_state_space

from .instance_data import InstanceData

from ..domain_data.domain_data import DomainData
from ..domain_data.domain_data_utils import compute_domain_data
from ..util.command import change_dir, write_file
from ..symmetries.exact import Driver


def compute_instance_datas(domain_filepath: Path,
                           instance_filepaths: List[Path],
                           disable_closed_Q: bool,
                           max_num_states_per_instance: int,
                           max_time_per_instance: int,
                           enable_dump_files: bool) -> Tuple[List[InstanceData], DomainData]:
    vocabulary_info = None
    instance_datas = []
    for i, instance_filepath in enumerate(instance_filepaths):
        name = instance_filepath.stem
        with change_dir(f"state_spaces/{name}"):
            logging.info("Constructing InstanceData for filename %s", instance_filepath)
            # change working directory to put planner output files in correct directory

            ## New code
            domain, problem, class_index_to_state, class_index_to_successor_class_indices = Driver(domain_filepath, instance_filepath, "INFO", False, False, False, 1).run()
            if vocabulary_info is None:
                # We obtain the parsed vocabulary from the first instance
                vocabulary_info = VocabularyInfo()
                for const in domain.constants:
                    vocabulary_info.add_constant(const.name)
                static_predicate_names = set(pred.name for pred in domain.static_predicates)
                for pred in domain.predicates:
                    if pred.name in static_predicate_names:
                        vocabulary_info.add_predicate(pred.name, pred.arity, True)
                    else:
                        vocabulary_info.add_predicate(pred.name, pred.arity, False)
                        vocabulary_info.add_predicate(pred.name + "_g", pred.arity, False)
                for typ in domain.types:
                    vocabulary_info.add_predicate(typ.name, 1)

                domain_data = compute_domain_data(str(domain_filepath), vocabulary_info)

            assert(vocabulary_info is not None)
            instance_info = InstanceInfo(i, vocabulary_info)
            for static_atom in problem.get_static_atoms():
                instance_info.add_static_atom(static_atom.predicate.name, [obj.name for obj in static_atom.terms])
            atom_to_dlplan_atom = dict()
            for atom in set(problem.get_encountered_atoms()).difference(set(problem.get_static_atoms())):
                atom_to_dlplan_atom[atom] = instance_info.add_atom(atom.predicate.name, [obj.name for obj in atom.terms])
            for literal in problem.goal:
                assert not literal.negated
                instance_info.add_static_atom(literal.atom.predicate.name + "_g", [obj.name for obj in literal.atom.terms])

            state_id = 0
            state_map = dict()
            for mimir_state in class_index_to_state.values():
                state_map[mimir_state] = state_id
                state_id += 1

            goal_state_ids = set()
            dlplan_states: Dict[int, State] = dict()
            for mimir_state in class_index_to_state.values():
                state_id = state_map[mimir_state]
                dlplan_states[state_id] = State(state_id, instance_info, [atom_to_dlplan_atom[atom] for atom in mimir_state.get_fluent_atoms()])
                if mimir_state.literals_hold(problem.goal):
                    goal_state_ids.add(state_id)

            forward_successors = defaultdict(set)
            for class_index, successor_class_indices in class_index_to_successor_class_indices.items():
                source_index = state_map[class_index_to_state[class_index]]
                for successor_class_index in successor_class_indices:
                    target_index = state_map[class_index_to_state[successor_class_index]]
                    forward_successors[source_index].add(target_index)

            state_space = StateSpace(instance_info, dlplan_states, 0, forward_successors, goal_state_ids)

            ## Old code
            #result = generate_state_space(str(domain_filepath), str(instance_filepath), vocabulary_info, len(instance_datas), max_time_per_instance)
            #if result.exit_code != GeneratorExitCode.COMPLETE:
            #    continue
            #state_space = result.state_space


            if vocabulary_info is None:
                # We obtain the parsed vocabulary from the first instance
                vocabulary_info = state_space.get_instance_info().get_vocabulary_info()
                domain_data = compute_domain_data(domain_filepath, vocabulary_info)
            if len(state_space.get_states()) > max_num_states_per_instance:
                continue
            goal_distances = state_space.compute_goal_distances()
            if goal_distances.get(state_space.get_initial_state_index(), None) is None:
                print("Unsolvable.")
                continue
            if set(state_space.get_states().keys()) == set(state_space.get_goal_state_indices()):
                print("Trivially solvable.")
                continue
            if disable_closed_Q and state_space.get_initial_state_index() in set(state_space.get_goal_state_indices()):
                print("Initial state is goal.")
                continue
            print("Num states:", len(state_space.get_states()))
            instance_data = InstanceData(len(instance_datas), domain_data, DenotationsCaches(), instance_filepath)
            instance_data.state_space = state_space

            if enable_dump_files:
                write_file(f"{name}.dot", state_space.to_dot(1))

            instance_data.goal_distances = goal_distances
            if disable_closed_Q:
                instance_data.initial_s_idxs = [state_space.get_initial_state_index(),]
            else:
                instance_data.initial_s_idxs = [s_idx for s_idx in state_space.get_states().keys() if instance_data.is_alive(s_idx)]
            print("initial state indices:", instance_data.initial_s_idxs)
            instance_datas.append(instance_data)
    # Sort the instances according to size and fix the indices afterwards
    instance_datas = sorted(instance_datas, key=lambda x : len(x.state_space.get_states()))
    for instance_idx, instance_data in enumerate(instance_datas):
        instance_data.id = instance_idx

    return instance_datas, domain_data
