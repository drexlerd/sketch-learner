from typing import Dict, Union
from dataclasses import dataclass, field

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


@dataclass
class PerTypeFeatures:
    """ Stores a collection of features accessible by repr or index. """
    f_idx_to_feature: Dict[int, Union[Boolean, Numerical]] = field(default_factory=dict)
    f_repr_to_feature: Dict[str, Union[Boolean, Numerical]] = field(default_factory=dict)

    def add_feature(self, feature: Feature):
        """ Adds and potentially overwrites an existing feature
        """
        self.f_idx_to_feature[feature.dlplan_feature.get_index()] = feature
        self.f_repr_to_feature[repr(feature.dlplan_feature)] = feature


@dataclass
class FeaturePool:
    """ Stores the generated pool of features. """
    boolean_features: PerTypeFeatures = field(default_factory=PerTypeFeatures)
    numerical_features: PerTypeFeatures = field(default_factory=PerTypeFeatures)
