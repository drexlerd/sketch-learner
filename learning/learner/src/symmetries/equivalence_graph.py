import json

from pathlib import Path
from typing import Dict, List, MutableSet

from dataclasses import dataclass, asdict, is_dataclass


def to_serializable(obj):
    """Convert a custom object to a serializable dictionary."""
    if is_dataclass(obj):
        return {k: to_serializable(v) for k, v in asdict(obj).items()}
    elif isinstance(obj, list):
        return [to_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, set):
        return [to_serializable(v) for v in obj]
    else:
        return obj


@dataclass
class Object:
    name: str

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return to_serializable({"name": self.name})

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other: "Object"):
        return self.name == other.name


@dataclass
class Constant:
    name: str

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return to_serializable({"name": self.name})

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other: "Constant"):
        return self.name == other.name

    def __lt__(self, other: "Constant"):
        return str(self) < str(other)


@dataclass
class Predicate:
    name: str
    arity: int

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return to_serializable({"name": self.name, "arity": self.arity})

    def __hash__(self):
        return hash((self.name, self.arity))

    def __eq__(self, other: "Predicate"):
        return self.name == other.name and self.arity == other.arity

    def __lt__(self, other: "Predicate"):
        return str(self) < str(other)


@dataclass
class Atom:
    predicate: Predicate
    objects: List[Object]

    @classmethod
    def from_dict(cls, data):
        predicate = Predicate.from_dict(data["predicate"])
        objects = [Object.from_dict(obj) for obj in data["objects"]]
        return cls(predicate, objects)

    def to_dict(self):
        return to_serializable({"predicate": self.predicate, "objects": self.objects})

    def __hash__(self):
        return hash((self.predicate, tuple(self.objects)))

    def __eq__(self, other: "Atom"):
        return self.predicate == other.predicate and self.objects == other.objects

    def __lt__(self, other: "Atom"):
        return str(self) < str(other)


@dataclass
class Literal:
    atom: Atom
    is_negated: bool

    @classmethod
    def from_dict(cls, data):
        atom = Atom.from_dict(data["atom"])
        is_negated = bool(data["is_negated"])
        return cls(atom, is_negated)

    def to_dict(self):
        return to_serializable({"atom": self.atom, "is_negated": self.is_negated})

    def __hash__(self):
        return hash((self.atom, self.is_negated))

    def __eq__(self, other: "Literal"):
        return self.atom == other.atom and self.is_negated == other.is_negated

    def __lt__(self, other: "Literal"):
        return str(self) < str(other)


@dataclass
class Domain:
    constants: List[Constant]
    predicates: List[Predicate]
    static_predicates: List[Predicate]

    @classmethod
    def from_dict(cls, data):
        constants = [Constant.from_dict(obj) for obj in data["constants"]]
        predicates = [Predicate.from_dict(obj) for obj in data["predicates"]]
        static_predicates = [Predicate.from_dict(obj) for obj in data["static_predicates"]]
        return cls(constants, predicates, static_predicates)

    def to_dict(self):
        return to_serializable({"constants": self.constants, "predicates": self.predicates, "static_predicates": self.static_predicates})

    def __hash__(self):
        return hash((tuple(sorted(self.constants)), tuple(sorted(self.predicates)), tuple(sorted(self.static_predicates))))

    def __eq__(self, other: "Domain"):
        return sorted(self.constants) == sorted(other.constants) and sorted(self.predicates) == sorted(other.predicates) and sorted(self.static_predicates) == sorted(other.static_predicates)


@dataclass
class Problem:
    encountered_atoms: List[Atom]
    static_atoms: List[Atom]
    goal_literals: List[Literal]

    @classmethod
    def from_dict(cls, data):
        encountered_atoms = [Atom.from_dict(obj) for obj in data["encountered_atoms"]]
        static_atoms = [Atom.from_dict(obj) for obj in data["static_atoms"]]
        goal_literals = [Literal.from_dict(obj) for obj in data["goal_literals"]]
        return cls(encountered_atoms, static_atoms, goal_literals)

    def to_dict(self):
        return to_serializable({"encountered_atoms": self.encountered_atoms, "static_atoms": self.static_atoms, "goal_literals": self.goal_literals})

    def __hash__(self):
        return hash((tuple(sorted(self.encountered_atoms)), tuple(sorted(self.static_atoms)), tuple(sorted(self.goal_literals))))

    def __eq__(self, other: "Problem"):
        return sorted(self.encountered_atoms) == sorted(other.encountered_atoms) and sorted(self.static_atoms) == sorted(other.static_atoms) and sorted(self.goal_literals) == sorted(other.goal_literals)


@dataclass
class State:
    index: int
    static_atoms: List[Atom]
    fluent_atoms: List[Atom]
    equivalence_class_index: int

    @classmethod
    def from_dict(cls, data):
        index = int(data["index"])
        static_atoms = [Atom.from_dict(obj) for obj in data["static_atoms"]]
        fluent_atoms = [Atom.from_dict(obj) for obj in data["fluent_atoms"]]
        equivalence_class_index = data["index"]
        return cls(index, static_atoms, fluent_atoms, equivalence_class_index)

    def to_dict(self):
        return to_serializable({"index": self.index, "static_atoms": self.static_atoms, "fluent_atoms": self.fluent_atoms, "equivalence_class_index": self.equivalence_class_index})

    def __hash__(self):
        return hash((self.index, tuple(sorted(self.static_atoms)), tuple(sorted(self.fluent_atoms)), self.equivalence_class_index))

    def __eq__(self, other: "State"):
        return self.index == other.index and sorted(self.static_atoms) == sorted(other.static_atoms) and sorted(self.fluent_atoms) == sorted(other.fluent_atoms) and sorted(self.equivalence_class_index) == sorted(other.equivalence_class_index)


@dataclass
class Action:
    name: str
    arguments: List[Object]

    @classmethod
    def from_dict(cls, data):
        name = data["name"]
        arguments = [Object.from_dict(obj) for obj in data["arguments"]]
        return cls(name, arguments)

    def to_dict(self):
        return to_serializable({"name": self.name, "arguments": self.arguments})

    def __hash__(self):
        return hash((self.name, tuple(self.arguments)))

    def __eq__(self, other: "Action"):
        return self.name == other.name and self.arguments == other.arguments



@dataclass
class Transition:
    source_index: int
    target_index: int
    action: Action

    @classmethod
    def from_dict(cls, data):
        source_index = int(data["source_index"])
        target_index = int(data["target_index"])
        action = Action.from_dict(data["action"])
        return cls(source_index, target_index, action)

    def to_dict(self):
        return to_serializable({"source_index": self.source_index, "target_index": self.target_index, "action": self.action})

    def __hash__(self):
        return hash((self.source_index, self.target_index, self.action))

    def __eq__(self, other: "Transition"):
        return self.source_index == other.source_index and self.target_index == other.target_index and self.action == other.action



class EquivalenceGraph:
    def __init__(self, domain: Domain, problem: Problem, states: Dict[int, State], transitions: Dict[int, List[Transition]], goal_states: MutableSet[int]):
        self.domain = domain
        self.problem = problem
        self.states = states
        self.transitions = transitions
        self.goal_states = goal_states

    @classmethod
    def from_dict(cls, data):
        domain = Domain.from_dict(data["domain"])
        problem = Problem.from_dict(data["problem"])
        states = {int(k): State.from_dict(v) for k, v in data["states"].items()}
        transitions = {int(k): [Transition.from_dict(t) for t in v] for k, v in data["transitions"].items()}
        goal_states = set(int(v) for v in data["goal_states"])
        return cls(domain, problem, states, transitions, goal_states)

    def to_dict(self):
        return to_serializable({
            "domain": self.domain,
            "problem": self.problem,
            "states": self.states,
            "transitions": self.transitions,
            "goal_states": self.goal_states
        })


def write_equivalence_graph(equivalence_graph: EquivalenceGraph, file_path: Path) -> None:
    """Write the state space to a file in JSON format."""
    with file_path.open('w') as f:
        json_dict = equivalence_graph.to_dict()
        f.write(json.dumps(json_dict, indent=4))


def read_equivalence_graph(file_path: Path) -> EquivalenceGraph:
    """Read the state space from a file in JSON format and update the instance."""
    with file_path.open() as f:
        data = json.load(f)
        return EquivalenceGraph.from_dict(data)
