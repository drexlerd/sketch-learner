from typing import List, Overload

from ..state_space import StateSpace


class NoveltyBase:
    def __init__(self, num_atoms: int, arity: int) -> None: ...
    def atom_indices_to_tuple_index(self, atom_indices: List[int]) -> int: ...
    def tuple_index_to_atom_indices(self, tuple_index: int) -> List[int]: ...
    def get_num_atoms(self) -> int: ...
    def get_arity(self) -> int: ...


class NoveltyTable:
    def __init__(self, novelty_base: NoveltyBase) -> None: ...
    @overload
    def compute_novel_tuple_indices(self, atom_indices: List[int]) -> List[int]: ...
    @overload
    def compute_novel_tuple_indices(self, atom_indices: List[int], add_atom_indices: List[int]) -> List[int]: ...
    @overload
    def insert_atom_indices(self, atom_indices: List[int], stop_if_novel: bool = False) -> bool: ...
    @overload
    def insert_atom_indices(self, atom_indices: List[int], add_atom_indices: List[int], stop_if_novel: bool = False) -> bool: ...
    @overload
    def insert_tuple_indices(self, tuple_indices: List[int], stop_if_novel: bool = False) -> bool: ...
    def resize(self, novelty_base: NoveltyBase) -> None: ...
    def get_novelty_base(self) -> NoveltyBase: ...


class TupleNode:
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def get_index(self) -> int: ...
    def get_tuple_index(self) -> int: ...
    def get_state_indices(self) -> List[int]: ...
    def get_predecessors(self) -> List[int]: ...
    def get_successors(self) -> List[int]: ...


class TupleGraph:
    def __init__(self, novelty_base: NoveltyBase, state_space: StateSpace, root_state_index: int) -> None: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def to_dot(self, verbosity_level: int) -> str: ...
    def get_novelty_base(self) -> NoveltyBase: ...
    def get_state_space(self) -> StateSpace: ...
    def get_root_state_index(self) -> int: ...
    def get_tuple_nodes(self) -> List[TupleNode]: ...
    def get_tuple_node_indices_by_distance(self) -> List[List[int]]: ...
    def get_state_indices_by_distance(self) -> List[List[int]]: ...