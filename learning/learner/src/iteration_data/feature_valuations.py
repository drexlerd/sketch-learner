from typing import Dict, Union, List
from dataclasses import dataclass


@dataclass
class FeatureValuations:
    f_idx_to_val: List[Union[bool, int]]


@dataclass
class PerStateFeatureValuations:
    s_idx_to_feature_valuations: Dict[int, FeatureValuations]
