from typing import Dict, List, MutableSet, Tuple
from dataclasses import dataclass, field

# Strategy 1:
# States s, s' with same feature valuation are in same abstract state A, i.e.,
# alpha(s) maps state to abstract state
# s, s' in A if for all f : f(s) = f(s')
# - abstract state A unsolvable if deadend state s is in A
# - termination is defined on abstract states
# - abstract state A is part of S*(s,t) if there exists state s' in A and s' in S*(s,t)

@dataclass
class EquivalenceData:
    # maps states pairs to key representing their equivalence class
    # class_key[s][s'] = key
    class_key: Dict[Tuple[int, int], ]
    # maps key to representative element of equivalence class
    # class_representative[key] = element

