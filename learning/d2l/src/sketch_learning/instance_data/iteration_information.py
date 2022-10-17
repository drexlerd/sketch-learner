from ast import Str
from ..util.command import create_experiment_workspace


class IterationInformation:
    def __init__(self, workspace: str, name: str, rm_if_existed=True):
        self.workspace = workspace
        self.feature_valuations_workspace = workspace / "feature_valuations"
        create_experiment_workspace(self.workspace, rm_if_existed)
        create_experiment_workspace(self.feature_valuations_workspace, rm_if_existed)
