from enum import Enum, unique


@unique
class ClingoExitCode(Enum):
    SATISFIABLE = 0
    UNSATISFIABLE = 1
    INTERRUPTED = 2
    UNKNOWN = 3
    EXHAUSTED = 4
