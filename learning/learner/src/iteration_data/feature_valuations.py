from typing import Dict
from dataclasses import dataclass, field


@dataclass
class FeatureValuations:
    b_idx_to_val: Dict[int, bool] = field(default_factory=dict)
    n_idx_to_val: Dict[int, int] = field(default_factory=dict)


@dataclass
class PerStateFeatureValuations:
    s_idx_to_feature_valuations: Dict[int, FeatureValuations] = field(default_factory=dict)
