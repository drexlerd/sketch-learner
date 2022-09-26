import dlplan

from collections import defaultdict
from dataclasses import dataclass
from typing import List

from sketch_learning.iteration_data.instance_feature_data import InstanceFeatureData

from .state_pair_equivalence import RuleEquivalences, StatePairEquivalence
from .domain_feature_data import DomainFeatureData

from ..instance_data.instance_data import InstanceData


@dataclass
class StatePairEquivalenceStatistics:
    num_equivalences: int = 0

    def increment_num_equivalences(self):
        self.num_equivalences += 1

    def print(self):
        print("Num equivalences:", self.num_equivalences)


class StateEquivalenceFactory:
    def __init__(self):
        self.statistics = StatePairEquivalenceStatistics()

    def make_state_equivalences(self, domain_feature_data: DomainFeatureData, instance_datas: List[InstanceData], instance_feature_datas: List[InstanceFeatureData]):
        pass
