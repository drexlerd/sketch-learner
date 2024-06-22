import logging
from typing import  List, Tuple, Dict, Union
from pathlib import Path
from collections import defaultdict

import pymimir as mm
import dlplan.core as dlplan_core
import dlplan.state_space as dlplan_statespace

from .instance_data import InstanceData

from ..domain_data.domain_data import DomainData
from ..domain_data.domain_data_utils import compute_domain_data
from ..util.command import change_dir, write_file


def create_vocabulary_info(domain: mm.Domain) -> dlplan_core.VocabularyInfo:
    vocabulary_info = dlplan_core.VocabularyInfo()
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
    return vocabulary_info


def create_instance_info(
        vocabulary_info: dlplan_core.VocabularyInfo,
        instance_id: int,
        mimir_state_space: mm.StateSpace
) -> Tuple[dlplan_core.InstanceInfo, Dict[Union[mm.FluentGroundAtom, mm.DerivedGroundAtom], dlplan_core.Atom]]:
    instance_info = dlplan_core.InstanceInfo(instance_id, vocabulary_info)
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
    return instance_info, atom_to_dlplan_atom


def create_dlplan_statespace(
        instance_info: dlplan_core.InstanceInfo,
        mimir_state_space: mm.StateSpace,
        atom_to_dlplan_atom: Dict[Union[mm.FluentGroundAtom, mm.DerivedGroundAtom], dlplan_core.Atom]
) -> dlplan_statespace.StateSpace:
    pddl_factories = mimir_state_space.get_aag().get_pddl_factories()
    dlplan_states: Dict[int, dlplan_core.State] = dict()
    forward_successors = defaultdict(set)
    for state_id, state in enumerate(mimir_state_space.get_states()):
        dlplan_state_atoms = []
        for atom in pddl_factories.get_fluent_ground_atoms_from_ids(state.get_fluent_atoms()):
            dlplan_state_atoms.append(atom_to_dlplan_atom[atom])
        for atom in pddl_factories.get_derived_ground_atoms_from_ids(state.get_derived_atoms()):
            dlplan_state_atoms.append(atom_to_dlplan_atom[atom])
        dlplan_states[state_id] = dlplan_core.State(state_id, instance_info, dlplan_state_atoms)
        for transition in mimir_state_space.get_forward_transitions()[state_id]:
            forward_successors[state_id].add(transition.get_successor_state())
    dlplan_state_space = dlplan_statespace.StateSpace(instance_info, dlplan_states, mimir_state_space.get_initial_state(), forward_successors, mimir_state_space.get_goal_states())
    return dlplan_state_space


def compute_instance_datas(domain_filepath: Path,
                           instance_filepaths: List[Path],
                           disable_closed_Q: bool,
                           max_num_states_per_instance: int,
                           max_time_per_instance: int,
                           enable_dump_files: bool) -> Tuple[List[InstanceData], DomainData]:
    instance_datas = []

    with change_dir("state_spaces", enable=enable_dump_files):
        # 1. Create mimir StateSpace and GlobalFaithfulAbstraction
        logging.info("Constructing GlobalFaithfulAbstractions...")
        abstractions = mm.GlobalFaithfulAbstraction.create(str(domain_filepath), [str(p) for p in instance_filepaths], False, True, max_num_states_per_instance, max_time_per_instance)
        logging.info("...done")
        if len(abstractions) == 0:
            return None, None

        logging.info("Constructing StateSpaces...")
        memories = []
        faithful_abstractions = abstractions[0].get_abstractions()
        for global_faithful_abstraction in faithful_abstractions:
            memories.append([global_faithful_abstraction.get_pddl_parser(), global_faithful_abstraction.get_aag(), global_faithful_abstraction.get_ssg()])
        state_spaces = mm.StateSpace.create(memories)
        logging.info("...done")

        # 2. Create DomainData
        vocabulary_info = create_vocabulary_info(state_spaces[0].get_aag().get_problem().get_domain())
        domain_data = compute_domain_data(str(domain_filepath), vocabulary_info)

        # 3. Create InstanceData
        for instance_id, (mimir_state_space, global_faithful_abstraction) in enumerate(zip(state_spaces, abstractions)):
            if mimir_state_space.get_num_goal_states() == 0:
                continue

            # 3.1. Create dlplan instance info
            instance_info, atom_to_dlplan_atom = create_instance_info(vocabulary_info, instance_id, mimir_state_space)

            # 3.2 Create dlplan state space
            dlplan_state_space = create_dlplan_statespace(instance_info, mimir_state_space, atom_to_dlplan_atom)

            # 3.3 Create mapping from concrete states to global faithful abstract states
            concrete_s_idx_to_global_s_idx = dict()
            for state_id, state in enumerate(mimir_state_space.get_states()):
                concrete_s_idx_to_global_s_idx[state_id] = global_faithful_abstraction.get_abstract_state_id(state)

            if enable_dump_files:
                write_file(f"{instance_id}.dot", dlplan_state_space.to_dot(1))

            if disable_closed_Q:
                initial_global_s_idxs = [global_faithful_abstraction.get_initial_state(),]
            else:
                initial_global_s_idxs = [s_idx for s_idx in range(global_faithful_abstraction.get_num_states()) if ((s_idx not in global_faithful_abstraction.get_goal_states()) and (s_idx not in global_faithful_abstraction.get_deadend_states()))]

            logging.info(f"Created InstanceData with num concrete states: {mimir_state_space.get_num_states()} and num abstract states: {global_faithful_abstraction.get_num_states()}")
            instance_data = InstanceData(instance_id, domain_data, dlplan_core.DenotationsCaches(), mimir_state_space.get_pddl_parser().get_problem_filepath(), global_faithful_abstraction, mimir_state_space, dlplan_state_space, concrete_s_idx_to_global_s_idx, initial_global_s_idxs)
            instance_datas.append(instance_data)

    # Sort the instances according to size and fix the indices afterwards
    # We also need to keep track of the remapping
    # for remapping FaithfulAbstractions within a GlobalFaithfulAbstraction.
    instance_datas = sorted(instance_datas, key=lambda x : x.global_faithful_abstraction.get_num_states())
    instance_idx_remap = [-1] * len(instance_datas)
    for new_instance_idx, instance_data in enumerate(instance_datas):
        instance_idx_remap[instance_data.idx] = new_instance_idx
    domain_data.instance_idx_remap = instance_idx_remap

    return instance_datas, domain_data
