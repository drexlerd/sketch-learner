from dataclasses import dataclass

from ..util.command import create_experiment_workspace


class InstanceInformation:
    def __init__(self, name: str, filename: str, workspace: str):
        self.name = name
        self.filename = filename
        self.workspace = workspace
        create_experiment_workspace(workspace, rm_if_existed=True)
