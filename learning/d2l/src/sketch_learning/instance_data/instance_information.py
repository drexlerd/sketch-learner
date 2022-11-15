from ..util.command import create_experiment_workspace


class InstanceInformation:
    def __init__(self, name: str, filename: str, workspace: str, rm_if_existed=True):
        self.name = name
        self.filename = filename
        self.workspace = workspace
        self.tuple_graph_workspace = workspace / "tuple_graphs"
        #create_experiment_workspace(self.workspace, rm_if_existed)
        #create_experiment_workspace(self.tuple_graph_workspace, rm_if_existed)
