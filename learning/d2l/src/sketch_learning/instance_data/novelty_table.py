import itertools


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
    def __init__(self, width, num_dynamic_atoms):
        self.table = [False for _ in range(num_dynamic_atoms ** width)]
        self.width = width
        self.num_dynamic_atoms = num_dynamic_atoms
        self.dimensions = [num_dynamic_atoms ** i for i in range(width)]

    def compute_t_idxs(self, atom_idxs):
        """ Compute all tuple indices for a state """
        assert all([atom_idx in range(self.num_dynamic_atoms) for atom_idx in atom_idxs])
        t_idxs = set()
        atom_idxs = self._pad_atom_ixs(atom_idxs)
        assert len(atom_idxs) >= self.width
        for t in itertools.combinations(atom_idxs, self.width):
            t = tuple(sorted(t))  # canonical representation
            assert t == self.idx2tuple(self._tuple2idx(sorted(t)))
            t_idxs.add(self._tuple2idx(sorted(t)))
        return t_idxs

    def compute_novel_t_idxs(self, atom_idxs):
        """ Compute all tuple indices for a state that are novel. """
        assert all([atom_idx in range(self.num_dynamic_atoms) for atom_idx in atom_idxs])
        t_idxs = self.compute_t_idxs(atom_idxs)
        novel_t_idxs = set()
        for t_idx in t_idxs:
            if self._is_novel(t_idx):
                novel_t_idxs.add(t_idx)
        return novel_t_idxs

    def mark_as_not_novel(self, t_idxs):
        """ Marks all tuple indices as not novel. """
        for t_idx in t_idxs:
            self.table[t_idx] = True

    def _pad_atom_ixs(self, atom_idxs):
        """ To be able to compute tuples of size k
        we need to pad atom_idxs to size k. """
        # Trick that allows us to compute t -> t_idx -> t
        # for t with len(t) < self.width
        if len(atom_idxs) < self.width:
            min_atom_idx = min(atom_idxs)
            atom_idxs.extend([min_atom_idx for _ in range(self.width - len(atom_idxs))])
        return atom_idxs

    def _is_novel(self, t_idx):
        """ Returns true iff the tuple is novel. """
        return not self.table[t_idx]

    def _tuple2idx(self, t):
        """ General version for tuples of arbitrary size (taken from LAPKT) """
        assert len(t) == self.width
        assert t == sorted(t)
        idx = 0
        for i in range(self.width):
            atom_idx = t[i]
            idx += atom_idx * self.dimensions[i]
        return idx

    def idx2tuple(self, t_idx):
        """ Inverse operation of tuple2idx """
        atom_idxs = []
        for i in reversed(range(self.width)):
            atom_idx = int(t_idx / self.dimensions[i])
            t_idx -= atom_idx * self.dimensions[i]
            atom_idxs.append(atom_idx)
        return tuple(sorted(atom_idxs))
