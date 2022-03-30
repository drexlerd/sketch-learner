import dlplan
import math

from typing import List, MutableSet, Dict
from dataclasses import dataclass, field
from collections import defaultdict, OrderedDict, deque

from .return_codes import ReturnCode
from ..util.command import read_file

class TransitionSystem:
    def __init__(self,
        states_by_index: List[dlplan.State],
        forward_transitions: Dict[int, List[int]],
        backward_transitions: Dict[int, List[int]],
        deadends: MutableSet[int],
        goals: MutableSet[int]):
        self.states_by_index = states_by_index
        self.forward_transitions = forward_transitions
        self.backward_transitions = backward_transitions
        self.deadends = deadends
        self.goals = goals

    def get_num_states(self):
        return len(self.states_by_index)

    def is_deadend(self, state_index: int):
        return state_index in self.deadends

    def is_goal(self, state_index: int):
        return state_index in self.goals

    def compute_states_by_distance(self, source: int):
        """ Perform BFS to partition states layerwise. """
        layers = OrderedDict()
        queue = deque()
        queue.append(source)
        distances = dict()
        distances[source] = 0
        while queue:
            curr_idx = queue.popleft()
            curr_cost = distances[curr_idx]
            layer = layers.setdefault(curr_cost, set())
            layer.add(curr_idx)
            # Stop upon reaching a goal:
            # Notice that we cannot stop upon reaching an deadend state since
            # those states contribute to novelty of states on goal paths.
            if curr_idx in self.goals: continue
            for succ_idx in self.forward_transitions[curr_idx]:
                succ_cost = distances.get(succ_idx, math.inf)
                if curr_cost + 1 < succ_cost:
                    if succ_idx not in distances:
                        queue.append(succ_idx)
                    distances[succ_idx] = curr_cost + 1
        return [list(l) for l in layers.values()]

    def print_statistics(self):
        print(f"Num states: {len(self.states_by_index)}")
        print(f"Num transitions: {sum([len(transitions) for transitions in self.forward_transitions.values()])}")
        print(f"Num deadends: {len(self.deadends)}")
        print(f"Num goals: {len(self.goals)}")

class TransitionSystemFactory:
    def __init__(self):
        pass

    def parse_transition_system(self, instance_info, state_space_filename):
        states = dict()
        forward_transitions = defaultdict(set)
        backward_transitions = defaultdict(set)
        deadends = set()
        goals = set()

        # Parse the header
        nlines = 0  # The number of useful lines processed
        static_atoms = []
        dynamic_atoms = []
        goal_atoms = []
        for line in read_file(state_space_filename):
            nlines += 1
            if line.startswith('(S)'):
                atom_name = line[4:]
                static_atoms.append(atom_name)
            elif line.startswith('(V)'):
                atom_name = line[4:]
                dynamic_atoms.append(atom_name)
            elif line.startswith('(G)'):
                atom_name = line[4:]
                if atom_name != "NOT-CONJUNCTIVE":
                    goal_atoms.append(atom_name)
            elif line.startswith('Unable to fully explore state space with max_expansions:'):
                return None, ReturnCode.EXHAUSTED_RESOURCES

        atom_name_to_dlplan_atom = dict()
        # add dynamic atoms first
        for atom_name in dynamic_atoms:
            normalized_atom_name = self._normalize_atom_name(atom_name)
            dlplan_atom = instance_info.add_atom(normalized_atom_name[0], normalized_atom_name[1:])
            atom_name_to_dlplan_atom[atom_name] = dlplan_atom
        for atom_name in static_atoms:
            normalized_atom_name = self._normalize_atom_name(atom_name)
            instance_info.add_static_atom(normalized_atom_name[0], normalized_atom_name[1:])
        for atom_name in goal_atoms:
            normalized_atom_name = self._normalize_atom_name(atom_name)
            instance_info.add_static_atom(normalized_atom_name[0] + "_g", normalized_atom_name[1:])

        # Parse the body
        for line in read_file(state_space_filename):
            if line.startswith('(E)'):  # An edge, with format "(E) 5 12"
                pid, cid = (int(x) for x in line[4:].split(' '))
                forward_transitions[pid].add(cid)
                backward_transitions[cid].add(pid)
                nlines += 1

            elif line.startswith('(N)'):  # A node
                # Format "(N) <id> <type> <space-separated-atom-list>", e.g.:
                # (N) 12 G
                elems = line[4:].split(' ')
                sid = int(elems[0])
                if elems[1] == 'G':  # The state is a goal state
                    goals.add(sid)
                if elems[1] == 'D':  # The state is a dead-end
                    deadends.add(sid)

                state_atoms = []
                for atom_name in elems[2:]:
                    dlplan_atom = atom_name_to_dlplan_atom[atom_name]
                    state_atoms.append(dlplan_atom)
                states[sid] = dlplan.State(instance_info, state_atoms)
        states_by_index = [None for i in range(len(states))]
        for s_idx, state in states.items():
            states_by_index[s_idx] = state
        if len(goals) == 0:
            return None, ReturnCode.UNSOLVABLE
        if len(goals) == len(states_by_index):
            return None, ReturnCode.TRIVIALLY_SOLVABLE
        return TransitionSystem(states_by_index, forward_transitions, backward_transitions, deadends, goals), ReturnCode.SOLVABLE

    def _normalize_atom_name(self, name):
        tmp = name.replace('()', '').replace(')', '').replace('(', ',')
        if "=" in tmp:  # We have a functional atom
            tmp = tmp.replace("=", ',')
        return tmp.split(',')