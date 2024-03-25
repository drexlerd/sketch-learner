from typing import Union, List
from dataclasses import dataclass

from dlplan.core import Boolean, Numerical


@dataclass
class Feature:
    """ A single feature with custom complexity. """
    _dlplan_feature: Union[Boolean, Numerical]
    _complexity: int

    @property
    def dlplan_feature(self):
        return self._dlplan_feature

    @property
    def complexity(self):
        return self._complexity

    def __eq__(self, other: "Feature"):
        return self.dlplan_feature == other.dlplan_feature

    def __hash__(self):
        return hash(str(self.dlplan_feature))


@dataclass
class FeaturePool:
    """ Stores the generated pool of features. """
    features: List[Feature]

