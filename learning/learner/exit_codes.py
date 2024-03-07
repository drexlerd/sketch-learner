from enum import Enum


class ExitCode(Enum):
    SUCCESS = 0
    UNKNOWN = 1
    UNSOLVABLE = 2
    INTERRUPTED = 2

