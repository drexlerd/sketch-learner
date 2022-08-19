from dataclasses import dataclass
from typing import Dict, List, MutableSet

from .novelty_base import NoveltyBase


@dataclass
class TupleGraph:
    def __init__(self,
        novelty_base: NoveltyBase,
        root_idx: int,
        t_idxs_by_distance: List[List[int]],
        s_idxs_by_distance: List[List[int]],
        t_idx_to_s_idxs: Dict[int, MutableSet[int]],
        s_idx_to_t_idxs: Dict[int, MutableSet[int]],
        width: int):
        assert len(s_idxs_by_distance) == len(t_idxs_by_distance)
        self.novelty_base = novelty_base
        self.root_idx = root_idx
        self.width = width
        self.t_idxs_by_distance = t_idxs_by_distance
        self.s_idxs_by_distance = s_idxs_by_distance
        self.t_idx_to_s_idxs = t_idx_to_s_idxs
        self.s_idx_to_t_idxs = s_idx_to_t_idxs

    def exists_admissible_chain_for(self, s_idxs : MutableSet[int]):
        """ Returns true iff there exists an admissible chain for s_idxs. """
        for s_idxs_2 in self.t_idx_to_s_idxs.values():
            if all(s_idx in s_idxs for s_idx in s_idxs_2):
                return True
        return False

    def t_idx_to_dlplan_atoms(self, t_idx: int):
        pass

    def print(self):
        print(f"Tuple graph for state {self.root_idx} and width {self.width}")
        print(f"t_idxs_by_distance: {self.t_idxs_by_distance}")
        print(f"s_idxs_by_distance: {self.s_idxs_by_distance}")
        print(f"t_idx_to_s_idxs: {self.t_idx_to_s_idxs}")
        print(f"s_idx_to_t_idxs: {self.s_idx_to_t_idxs}")
