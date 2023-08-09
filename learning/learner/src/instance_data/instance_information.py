from pathlib import Path


class InstanceInformation:
    def __init__(self, name: str, filename: str, workspace: Path):
        self.name = name
        self.filename = filename
        self.workspace = workspace
