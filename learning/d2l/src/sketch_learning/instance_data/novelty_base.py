import dlplan
import itertools
from typing import List


class NoveltyBase:
    def __init__(self, width, dlplan_atoms: List[dlplan.Atom]):
        self.width = width
        self.dlplan_atoms = dlplan_atoms
        self.num_atoms = len(dlplan_atoms) + 1  # we map atom_idx=len(dlplan_atoms) to the empty atom
        self.dimensions = [self.num_atoms ** i for i in range(width)]

    def compute_tuples(self, atom_idxs: List[int]):
        """ Compute all tuple indices for a state """
        assert all([atom_idx in range(self.num_atoms - 1) for atom_idx in atom_idxs])
        t_idxs = set()
        for t in itertools.combinations(atom_idxs, min(len(atom_idxs), self.width)):
            t = sorted(t)  # canonical representation, t is list
            t_idx = self.atom_idxs_to_tuple_idx(t)
            t_idxs.add(t_idx)
            assert t == self.tuple_idx_to_atom_idxs(t_idx)
        return t_idxs

    def pad_atom_idxs(self, atom_idxs: List[int]):
        """ To be able to compute tuples of size k
        we need to pad atom_idxs to size k. """
        atom_idxs.extend([(self.num_atoms - 1) for _ in range(self.width - len(atom_idxs))])
        assert len(atom_idxs) == self.width
        return atom_idxs

    def atom_idxs_to_tuple_idx(self, atom_idxs: List[int]):
        """ General version for tuples of arbitrary size (taken from LAPKT) """
        self.pad_atom_idxs(atom_idxs)
        assert len(atom_idxs) == self.width
        assert atom_idxs == sorted(atom_idxs)
        idx = 0
        for i in range(self.width):
            atom_idx = atom_idxs[i]
            idx += atom_idx * self.dimensions[i]
        return idx

    def tuple_idx_to_atom_idxs(self, t_idx: int):
        """ Inverse operation of tuple2idx """
        assert isinstance(t_idx, int)
        atom_idxs = []
        for i in reversed(range(self.width)):
            atom_idx = int(t_idx / self.dimensions[i])
            t_idx -= atom_idx * self.dimensions[i]
            atom_idxs.append(atom_idx)
        return sorted(atom_idxs)

    def tuple_idx_to_dplan_atoms(self, t_idx: int):
        assert isinstance(t_idx, int)
        atom_idxs = self.tuple_idx_to_atom_idxs(t_idx)
        return [self.dlplan_atoms[atom_idx] for atom_idx in atom_idxs if atom_idx != self.num_atoms]
