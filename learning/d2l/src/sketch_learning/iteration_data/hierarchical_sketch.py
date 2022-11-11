from termcolor import colored

from .sketch import Sketch

from ..util.command import create_experiment_workspace, read_file, write_file

class HierarchicalSketch:
    def __init__(self, sketch: Sketch, workspace: str, parent=None):
        self.sketch = sketch
        self.parent = parent
        self.children = []
        self.workspace = workspace
        create_experiment_workspace(self.workspace, rm_if_existed=True)
        write_file(self.workspace / f"sketch_{self.sketch.width}.txt", self.sketch.dlplan_policy.compute_repr())

    def add_child(self, sketch, folder):
        child = HierarchicalSketch(sketch, self.workspace / folder, self)
        self.children.append(child)
        return child

    def print(self):
        level = 0
        self.print_rec(level)

    def print_rec(self, level):
        print(colored("    " * level + f"Level {level} sketch:", "green", "on_grey"))
        print(self.sketch.dlplan_policy.compute_repr())
        for child in self.children:
            child.print_rec(level+1)

    def collect_features(self):
        features = []
        if self.children:
            for child in self.children:
                features.extend(child.collect_features())
        features.extend(self.sketch.dlplan_policy.get_boolean_features())
        features.extend(self.sketch.dlplan_policy.get_numerical_features())
        return features

    def collect_rules(self):
        rules = []
        if self.children:
            for child in self.children:
                rules.extend(self.collect_rules())
        rules.extend(self.sketch.dlplan_policy.get_rules())
        return rules

