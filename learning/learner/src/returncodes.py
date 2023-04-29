"""
    The possible exit codes of the pipeline components.
"""
from enum import Enum, unique


@unique
class ExitCode(Enum):
    Success = 0
    Unsatisfiable = 1

    OutOfMemory = 100
    OutOfTime = 101
