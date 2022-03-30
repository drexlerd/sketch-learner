import re
from enum import Enum

from typing import Dict, List, MutableSet
from dataclasses import dataclass, field


class AnswerSetParser_ExitCode(Enum):
    Satisfiable = 0
    Unsatisfiable = 1


@dataclass
class AnswerSetData:
    facts: List[str]
    optimization_value: int


class AnswerSetParser:
    def parse(self, answer_set_file_content):
        """ Parses facts and optimization value of all answer sets and return them if satisfiable.
            Otherwise report that the ASP is unsatisfiable. """
        answer_set_datas = []
        exitcode = AnswerSetParser_ExitCode.Satisfiable
        while True:
            line = next(answer_set_file_content, None)
            if line is None: break
            if line.startswith("clingo version"):
                pass
            # elif line.startswith("Solving..."):
            #    pass
            elif line.startswith("UNSATISFIABLE"):
                exitcode = AnswerSetParser_ExitCode.Unsatisfiable
                break
            elif line.startswith("Answer: "):
                facts = next(answer_set_file_content).split(" ")
                optimization_value = int(re.findall("Optimization: (\d+)", next(answer_set_file_content))[0])
                answer_set_datas.append(AnswerSetData(facts, optimization_value))
        return answer_set_datas, exitcode