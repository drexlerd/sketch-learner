from typing import Dict, List, MutableSet, Tuple
from dataclasses import dataclass, field

# Strategy 1:
# States s, s' with same feature valuation are in same abstract state A
# s ~ s' in same abstract state A, i.e. s,s' in A if for all f : f(s) = f(s')

@dataclass
class EquivalenceData:
    # maps states pairs to key representing their equivalence class
    # class_key[s][s'] = key
    class_key: Dict[Tuple[int, int], ]
    # maps key to representative element of equivalence class
    # class_representative[key] = element

