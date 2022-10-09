import dlplan

from typing import List
from dataclasses import dataclass


@dataclass
class DomainFeatureData:
    """ DomainFeatureData stores all novel Boolean and Numerical features for a set of dlplan states. """
    boolean_features: List[dlplan.Boolean]
    numerical_features: List[dlplan.Numerical]

    def print(self):
        print("Domain feature data:")
        print(f"    Boolean features: {self.boolean_features}")
        print(f"    Numerical features: {self.numerical_features}")
