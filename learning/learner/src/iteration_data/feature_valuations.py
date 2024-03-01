from typing import Dict, Union, List
from dataclasses import dataclass, field


@dataclass
class FeatureValuations:
    feature_valuations: List[Union[bool, int]] = field(default_factory=list)


@dataclass
class PerStateFeatureValuations:
    s_idx_to_feature_valuations: Dict[int, FeatureValuations] = field(default_factory=dict)
