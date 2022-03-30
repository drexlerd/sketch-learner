from enum import Enum


class ReturnCode(Enum):
    TRIVIALLY_SOLVABLE = 0
    SOLVABLE = 1
    UNSOLVABLE = 2
    EXHAUSTED_RESOURCES = 3