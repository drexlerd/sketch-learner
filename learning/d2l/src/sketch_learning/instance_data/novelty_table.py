from typing import List

from .novelty_base import NoveltyBase


class NoveltyTable():
    """ The novelty table tracks novelty status of tuples.
        An example for width=2, num_dynamic_atoms=2:
        Function f:|A|x|A|->N maps 2-tuples of atoms to an index.
        f s1 s2
        0  0  0
        1  0  1
        2  0  2  (a0) -> 2
        3  1  0  (a1, a0) -> (a0, a1) -> 1
        4  1  1
        5  1  2  (a1, a2) -> 5
        6  2  0
        7  2  1
        8  2  2
    """
    def __init__(self, novelty_base: NoveltyBase):
        self.novelty_base = novelty_base
        self.table = [False for _ in range(self.novelty_base.num_atoms ** self.novelty_base.width)]

    def compute_novel_tuples(self, atom_idxs: List[int]):
        """ Compute all tuple indices for a state that are novel. """
        assert all([atom_idx in range(self.novelty_base.num_atoms - 1) for atom_idx in atom_idxs])
        t_idxs = self.novelty_base.compute_tuples(atom_idxs)
        novel_t_idxs = set()
        for t_idx in t_idxs:
            if not self.table[t_idx]:
                novel_t_idxs.add(t_idx)
        return novel_t_idxs

    def mark_as_not_novel(self, t_idxs: List[int]):
        """ Marks all tuple indices as not novel. """
        for t_idx in t_idxs:
            self.table[t_idx] = True
