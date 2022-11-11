from ast import Str
from ..util.command import create_experiment_workspace


class IterationInformation:
    def __init__(self, workspace: str, name: str, rm_if_existed=True):
        self.workspace = workspace
        self.tuple_graph_workspace = workspace / "tuple_graphs"
        self.feature_valuations_workspace = workspace / "feature_valuations"
        self.state_equivalence_workspace = workspace / "state_equivalence"
        self.state_pair_equivalence_workspace = workspace / "state_pair_equivalence"
        self.tuple_graph_equivalences_workspace = workspace / "tuple_graph_equivalences"
        #create_experiment_workspace(self.workspace, rm_if_existed)
        #create_experiment_workspace(self.tuple_graph_workspace, rm_if_existed)
        #create_experiment_workspace(self.feature_valuations_workspace, rm_if_existed)
        #create_experiment_workspace(self.state_equivalence_workspace, rm_if_existed)
        #create_experiment_workspace(self.state_pair_equivalence_workspace, rm_if_existed)
        #create_experiment_workspace(self.tuple_graph_equivalences_workspace, rm_if_existed)
