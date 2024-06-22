import logging
from typing import  List, Tuple, Dict
from pathlib import Path
from collections import defaultdict

import pymimir as mm
import dlplan.core as dlcore
import dlplan.state_space as dlstatespace

from .instance_data import InstanceData

from ..domain_data.domain_data import DomainData
from ..domain_data.domain_data_utils import compute_domain_data
from ..util.command import change_dir, write_file

def compute_instance_datas(domain_filepath: Path,
                           instance_filepaths: List[Path],
                           disable_closed_Q: bool,
                           max_num_states_per_instance: int,
                           max_time_per_instance: int,
                           enable_dump_files: bool) -> Tuple[List[InstanceData], DomainData]:
    instance_datas = []

    with change_dir("state_spaces", enable=enable_dump_files):
        abstractions = mm.GlobalFaithfulAbstraction.create(str(domain_filepath), [str(p) for p in instance_filepaths], False, True, max_num_states_per_instance, max_time_per_instance)
        memories = []
        faithful_abstractions = abstractions[0].get_abstractions()
        for global_faithful_abstraction in faithful_abstractions:
            memories.append([global_faithful_abstraction.get_pddl_parser(), global_faithful_abstraction.get_aag(), global_faithful_abstraction.get_ssg()])
        state_spaces = mm.StateSpace.create(memories)

        vocabulary_info = dlcore.VocabularyInfo()
        problem = state_spaces[0].get_aag().get_problem()
        domain = problem.get_domain()
        for predicate in domain.get_static_predicates():
            if predicate.get_name() != "=":
                vocabulary_info.add_predicate(predicate.get_name(), len(predicate.get_parameters()), True)
                vocabulary_info.add_predicate(predicate.get_name() + "_g", len(predicate.get_parameters()), True)
        for predicate in domain.get_fluent_predicates():
            vocabulary_info.add_predicate(predicate.get_name(), len(predicate.get_parameters()), False)
            vocabulary_info.add_predicate(predicate.get_name() + "_g", len(predicate.get_parameters()), False)
        for predicate in domain.get_derived_predicates():
            vocabulary_info.add_predicate(predicate.get_name(), len(predicate.get_parameters()), False)
            vocabulary_info.add_predicate(predicate.get_name() + "_g", len(predicate.get_parameters()), False)
        for obj in domain.get_constants():
            vocabulary_info.add_constant(obj.get_name())
        domain_data = compute_domain_data(str(domain_filepath), vocabulary_info)

        for instance_id, (mimir_state_space, global_faithful_abstraction) in enumerate(zip(state_spaces, abstractions)):
            if mimir_state_space.get_num_goal_states() == 0:
                continue

            instance_info = dlcore.InstanceInfo(instance_id, vocabulary_info)
            pddl_factories = mimir_state_space.get_aag().get_pddl_factories()
            problem = mimir_state_space.get_aag().get_problem()
            # Static initial literals
            for literal in problem.get_static_initial_literals():
                if literal.get_atom().get_predicate().get_name() != "=":
                    assert not literal.is_negated()
                    instance_info.add_static_atom(literal.get_atom().get_predicate().get_name(), [obj.get_name() for obj in literal.get_atom().get_objects()])
            for literal in problem.get_fluent_initial_literals():
                assert not literal.is_negated()
                instance_info.add_static_atom(literal.get_atom().get_predicate().get_name(), [obj.get_name() for obj in literal.get_atom().get_objects()])
            # Reached atoms
            atom_to_dlplan_atom = dict()
            for atom in pddl_factories.get_fluent_ground_atoms_from_ids(mimir_state_space.get_ssg().get_reached_fluent_ground_atoms()):
                atom_to_dlplan_atom[atom] = instance_info.add_atom(atom.get_predicate().get_name(), [obj.get_name() for obj in atom.get_objects()])
            for atom in pddl_factories.get_derived_ground_atoms_from_ids(mimir_state_space.get_ssg().get_reached_derived_ground_atoms()):
                atom_to_dlplan_atom[atom] = instance_info.add_atom(atom.get_predicate().get_name(), [obj.get_name() for obj in atom.get_objects()])
            # Goal literals
            for literal in problem.get_static_goal_condition():
                assert not literal.is_negated()
                instance_info.add_static_atom(literal.get_atom().get_predicate().get_name() + "_g", [obj.get_name() for obj in literal.get_atom().get_objects()])
            for literal in problem.get_fluent_goal_condition():
                assert not literal.is_negated()
                instance_info.add_static_atom(literal.get_atom().get_predicate().get_name() + "_g", [obj.get_name() for obj in literal.get_atom().get_objects()])
            for literal in problem.get_derived_goal_condition():
                assert not literal.is_negated()
                instance_info.add_static_atom(literal.get_atom().get_predicate().get_name() + "_g", [obj.get_name() for obj in literal.get_atom().get_objects()])

            # Create complete state space and mapping to abstract statess
            dlplan_states: Dict[int, dlcore.State] = dict()
            forward_successors = defaultdict(set)
            state_index_to_representative_state_index = dict()
            for state_id, state in enumerate(mimir_state_space.get_states()):
                state_index_to_representative_state_index[state_id] = global_faithful_abstraction.get_abstract_state_id(state)
                dlplan_state_atoms = []
                for atom in pddl_factories.get_fluent_ground_atoms_from_ids(state.get_fluent_atoms()):
                    dlplan_state_atoms.append(atom_to_dlplan_atom[atom])
                for atom in pddl_factories.get_derived_ground_atoms_from_ids(state.get_derived_atoms()):
                    dlplan_state_atoms.append(atom_to_dlplan_atom[atom])
                dlplan_states[state_id] = dlcore.State(state_id, instance_info, dlplan_state_atoms)
                for transition in mimir_state_space.get_forward_transitions()[state_id]:
                    forward_successors[state_id].add(transition.get_successor_state())

            dlplan_state_space = dlstatespace.StateSpace(instance_info, dlplan_states, mimir_state_space.get_initial_state(), forward_successors, mimir_state_space.get_goal_states())

            if enable_dump_files:
                write_file(f"{instance_id}.dot", dlplan_state_space.to_dot(1))

            if disable_closed_Q:
                initial_s_idxs = [mimir_state_space.get_initial_state(),]
            else:
                initial_s_idxs = [s_idx for s_idx in range(mimir_state_space.get_num_states()) if ((s_idx not in mimir_state_space.get_goal_states()) and (s_idx not in mimir_state_space.get_deadend_states()))]

            instance_data = InstanceData(instance_id, domain_data, dlcore.DenotationsCaches(), mimir_state_space.get_pddl_parser().get_problem_filepath(), global_faithful_abstraction, mimir_state_space, dlplan_state_space, state_index_to_representative_state_index, initial_s_idxs)
            instance_datas.append(instance_data)
    # Sort the instances according to size and fix the indices afterwards
    instance_datas = sorted(instance_datas, key=lambda x : x.mimir_state_space.get_num_states())
    for instance_idx, instance_data in enumerate(instance_datas):
        instance_data.id = instance_idx

    return instance_datas, domain_data
