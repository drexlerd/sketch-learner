from typing import Dict, List
from dataclasses import dataclass


@dataclass
class InstanceFeatureData:
    """ InstanceFeatureData stores feature valuations for each state in an instance. """
    boolean_feature_valuations: Dict[int, List[bool]]
    numerical_feature_valuations: Dict[int, List[int]]

    def print(self):
        print("Instance feature data:")
        print(f"    Boolean feature valuations: {self.boolean_feature_valuations}")
        print(f"    Numerical feature valuations: {self.numerical_feature_valuations}")
