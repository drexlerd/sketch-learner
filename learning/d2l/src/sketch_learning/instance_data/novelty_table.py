import dlplan
import itertools
from typing import List
from dataclasses import dataclass


@dataclass
class Tuple:
    index: int
    atoms: List[dlplan.Atom]

    def __str__(self):
        return "{" + ", ".join([atom.get_name() for atom in self.atoms]) + "}"


class NoveltyTable:
    """ The novelty table tracks novelty status of tuples.
        An example for width=2, num_dynamic_atoms=2:
        Function f:|A|x|A|->N maps 2-tuples of atoms to an index.
        f a0 a1
        0  0  0
        1  0  1
        2  1  0
        3  1  1
    """
    def __init__(self, width, atoms):
        self.width = width
        self.atom = atoms
        self.num_atoms = len(atoms)
        self.table = [False for _ in range(self.num_atoms ** width)]
        self.dimensions = [self.num_atoms ** i for i in range(width)]

    def compute_tuples(self, atom_idxs: List[int]):
        """ Compute all tuple indices for a state """
        assert all([atom_idx in range(self.num_atoms) for atom_idx in atom_idxs])
        t_idxs = set()
        atom_idxs = self._pad_atom_idxs(atom_idxs)
        assert len(atom_idxs) >= self.width
        for t in itertools.combinations(atom_idxs, self.width):
            t = tuple(sorted(t))  # canonical representation
            assert t == self.tuple_idx_to_atom_idxs(self.atom_idxs_to_tuple_idx(sorted(t)))
            t_idxs.add(self.atom_idxs_to_tuple_idx(sorted(t)))
        return t_idxs

    def compute_novel_tuples(self, atom_idxs: List[int]):
        """ Compute all tuple indices for a state that are novel. """
        assert all([atom_idx in range(self.num_atoms) for atom_idx in atom_idxs])
        t_idxs = self.compute_tuples(atom_idxs)
        novel_t_idxs = set()
        for t_idx in t_idxs:
            if not self.table[t_idx]:
                novel_t_idxs.add(t_idx)
        return novel_t_idxs

    def mark_as_not_novel(self, tuples: List[Tuple]):
        """ Marks all tuple indices as not novel. """
        for tuple in tuples:
            self.table[tuple] = True

    def _pad_atom_idxs(self, atom_idxs):
        """ To be able to compute tuples of size k
        we need to pad atom_idxs to size k. """
        # Trick that allows us to compute t -> t_idx -> t
        # for t with len(t) < self.width
        if len(atom_idxs) < self.width:
            min_atom_idx = min(atom_idxs)
            atom_idxs.extend([min_atom_idx for _ in range(self.width - len(atom_idxs))])
        return atom_idxs

    def atom_idxs_to_tuple_idx(self, atom_idxs: List[int]):
        """ General version for tuples of arbitrary size (taken from LAPKT) """
        assert len(atom_idxs) == self.width
        assert atom_idxs == sorted(atom_idxs)
        idx = 0
        for i in range(self.width):
            atom_idx = atom_idxs[i]
            idx += atom_idx * self.dimensions[i]
        return idx

    def tuple_idx_to_atom_idxs(self, t_idx: int):
        """ Inverse operation of tuple2idx """
        atom_idxs = []
        for i in reversed(range(self.width)):
            atom_idx = int(t_idx / self.dimensions[i])
            t_idx -= atom_idx * self.dimensions[i]
            atom_idxs.append(atom_idx)
        return tuple(sorted(atom_idxs))
