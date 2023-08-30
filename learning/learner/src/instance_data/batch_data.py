import ast
from dataclasses import dataclass
from typing import List

from dlplan.serialization import Data, serialize, deserialize

from learner.src.domain_data.domain_data import DomainData
from learner.src.domain_data.domain_data_utils import construct_feature_generator
from learner.src.instance_data.instance_data import InstanceData


def parse_tuple(t: str):
    return ast.literal_eval(t)


@dataclass
class BatchData:
    """ Stores all information necessary for serialization and deserialization of InstanceDatas.

    We could also serialize the whole program state to be able to restart
    the whole pipeline during each intermediate step.
    """
    domain_data: DomainData
    instance_datas: List[InstanceData]

    def __getstate__(self):
        """ Serializes the collection of InstanceData.
            Only attributes that remain constant in each iteration are serialized.
        """
        state = dict()

        # DomainData
        state["domain_filename"] = self.domain_data.domain_filename
        vocabulary_infos = dict()
        vocabulary_infos["0"] = self.domain_data.vocabulary_info
        policy_builders = dict()
        policy_builders["0"] = self.domain_data.policy_builder
        syntactic_element_factories = dict()
        syntactic_element_factories["0"] = self.domain_data.syntactic_element_factory
        state["domain_feature_data"] = self.domain_data.domain_feature_data
        state["domain_state_pair_equivalence"] = self.domain_data.domain_state_pair_equivalence

        # Flatten InstanceInfos
        ids = []
        instance_informations = []
        goal_distances = []
        state_spaces = dict()
        tuple_graphs = dict()
        denotations_caches = dict()
        initial_s_idxs = dict()
        per_state_feature_valuations = dict()
        per_state_state_pair_equivalences = dict()
        per_state_tuple_graph_equivalences = dict()
        for i, instance_data in enumerate(self.instance_datas):
            ids.append(instance_data.id)
            instance_informations.append(instance_data.instance_information)
            goal_distances.append(instance_data.goal_distances)
            state_spaces[str(i)] = instance_data.state_space
            denotations_caches[str(i)] = instance_data.denotations_caches
            if instance_data.per_state_tuple_graphs is not None:
                for s_idx, tuple_graph in instance_data.per_state_tuple_graphs.items():
                    tuple_graphs[str((i, s_idx))] = tuple_graph
            initial_s_idxs[str(i)] = instance_data.initial_s_idxs
            per_state_feature_valuations[str(i)] = instance_data.per_state_feature_valuations
            per_state_state_pair_equivalences[str(i)] = instance_data.per_state_state_pair_equivalences
            per_state_tuple_graph_equivalences[str(i)] = instance_data.per_state_tuple_graph_equivalences
        state["ids"] = ids
        state["num_instances"] = len(self.instance_datas)
        state["instance_informations"] = instance_informations
        state["goal_distances"] = goal_distances
        state["initial_s_idxs"] = initial_s_idxs
        state["per_state_feature_valuations"] = per_state_feature_valuations
        state["per_state_state_pair_equivalences"] = per_state_state_pair_equivalences
        state["per_state_tuple_graph_equivalences"] = per_state_tuple_graph_equivalences

        # Serialize DLPlan related data.
        data = Data()
        data.vocabulary_infos = vocabulary_infos
        data.policy_builders = policy_builders
        data.syntactic_element_factories = syntactic_element_factories
        data.state_spaces = state_spaces
        data.tuple_graphs = tuple_graphs
        data.denotations_caches = denotations_caches
        state["data"] = serialize(data)
        return state

    def __setstate__(self, state):
        """ Deserializes a collection of InstanceData.
            Only attributes that remain constant in each iteration are deserialized.
        """
        data = deserialize(state["data"])
        # DomainData
        vocabulary_info = data.vocabulary_infos["0"]
        policy_builder = data.policy_builders["0"]
        syntactic_element_factory = data.syntactic_element_factories["0"]
        feature_generator = construct_feature_generator()
        domain_feature_data = state["domain_feature_data"]
        domain_state_pair_equivalence = state["domain_state_pair_equivalence"]
        self.domain_data = DomainData(state["domain_filename"], vocabulary_info, policy_builder, syntactic_element_factory, feature_generator, domain_feature_data, domain_state_pair_equivalence)
        # InstanceData
        self.instance_datas = []
        num_instances = state["num_instances"]
        for i in range(num_instances):
            tuple_graphs = { ast.literal_eval(key)[1]: tuple_graph for key, tuple_graph in data.tuple_graphs if ast.literal_eval(key)[0] == i}
            self.instance_datas.append(
                InstanceData(
                    state["ids"][i],
                    self.domain_data,
                    data.denotations_caches[str(i)],
                    state["instance_informations"][i],
                    data.state_spaces[str(i)],
                    state["goal_distances"][i],
                    tuple_graphs,
                    state["initial_s_idxs"][str(i)],
                    state["per_state_feature_valuations"][str(i)],
                    state["per_state_state_pair_equivalences"][str(i)],
                    state["per_state_tuple_graph_equivalences"][str(i)]))


