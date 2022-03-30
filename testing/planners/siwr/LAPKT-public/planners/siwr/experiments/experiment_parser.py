"""
Plan found with cost: 79
1. (pick ball1 rooma left)
2. (move rooma roomb)
3. (drop ball1 roomb left)
4. (move roomb rooma)
5. (pick ball10 rooma left)
6. (move rooma roomb)
7. (drop ball10 roomb left)
8. (move roomb rooma)
9. (pick ball11 rooma left)
10. (move rooma roomb)
11. (drop ball11 roomb left)
12. (move roomb rooma)
13. (pick ball12 rooma left)
14. (move rooma roomb)
15. (drop ball12 roomb left)
16. (move roomb rooma)
17. (pick ball13 rooma left)
18. (move rooma roomb)
19. (drop ball13 roomb left)
20. (move roomb rooma)
21. (pick ball14 rooma left)
22. (move rooma roomb)
23. (drop ball14 roomb left)
24. (move roomb rooma)
25. (pick ball15 rooma left)
26. (move rooma roomb)
27. (drop ball15 roomb left)
28. (move roomb rooma)
29. (pick ball16 rooma left)
30. (move rooma roomb)
31. (drop ball16 roomb left)
32. (move roomb rooma)
33. (pick ball17 rooma left)
34. (move rooma roomb)
35. (drop ball17 roomb left)
36. (move roomb rooma)
37. (pick ball19 rooma left)
38. (move rooma roomb)
39. (drop ball19 roomb left)
40. (move roomb rooma)
41. (pick ball18 rooma left)
42. (move rooma roomb)
43. (drop ball18 roomb left)
44. (move roomb rooma)
45. (pick ball2 rooma left)
46. (move rooma roomb)
47. (drop ball2 roomb left)
48. (move roomb rooma)
49. (pick ball20 rooma left)
50. (move rooma roomb)
51. (drop ball20 roomb left)
52. (move roomb rooma)
53. (pick ball3 rooma left)
54. (move rooma roomb)
55. (drop ball3 roomb left)
56. (move roomb rooma)
57. (pick ball5 rooma left)
58. (move rooma roomb)
59. (drop ball5 roomb left)
60. (move roomb rooma)
61. (pick ball4 rooma left)
62. (move rooma roomb)
63. (drop ball4 roomb left)
64. (move roomb rooma)
65. (pick ball6 rooma left)
66. (move rooma roomb)
67. (drop ball6 roomb left)
68. (move roomb rooma)
69. (pick ball7 rooma left)
70. (move rooma roomb)
71. (drop ball7 roomb left)
72. (move roomb rooma)
73. (pick ball8 rooma left)
74. (move rooma roomb)
75. (drop ball8 roomb left)
76. (move roomb rooma)
77. (pick ball9 rooma left)
78. (move rooma roomb)
79. (drop ball9 roomb left)

Time: 0.296746
Generated: 10292
Expanded: 4377
Total time: 0.296754
Nodes generated during search: 10293
Nodes expanded during search: 4377
Nodes pruned by bound: 17565
Average ef. width: 2
Max ef. width: 2
IW search completed in 0.296754 secs, check 'iw.log' for details
"""



from email.policy import default
import math
import re

from lab.parser import Parser


def error(content, props):
    if props["planner_exit_code"] == 0:
        props["error"] = "plan-found"
    else:
        props["error"] = "unsolvable-or-error"


def coverage(content, props):
    props["coverage"] = int(props.get("cost", None) is not None)

def get_plan(content, props):
    # All patterns are parsed before functions are called.
    if props.get("evaluations") is not None:
        props["plan"] = re.findall(r"^(?:step)?\s*\d+: (.+)$", content, re.M)


def get_times(content, props):
    props["times"] = re.findall(r"(\d+\.\d+) seconds", content)


def trivially_unsolvable(content, props):
    props["trivially_unsolvable"] = int(
        "ff: goal can be simplified to FALSE. No plan will solve it" in content
    )

def adapt_average_effective_width(content, props):
    if props.get("width_average", None) is not None and \
        math.isnan(props["width_average"]):
        props["width_average"] = float("inf")

def not_i_reachable(content, props):
    props["not_i_reachable"] = int(";; NOT I-REACHABLE ;;" in content)


parser = Parser()
parser.add_pattern("node", r"node: (.+)\n", type=str, file="driver.log", required=True)
parser.add_pattern(
    "planner_exit_code", r"run-planner exit code: (.+)\n", type=int, file="driver.log"
)
parser.add_pattern("cost", r"Plan found with cost: (\d+)", type=int)
parser.add_pattern("total_time", r"Total time: (.+)", type=float)
parser.add_pattern("nodes_generated", r"Nodes generated during search: (\d+)", type=int)
parser.add_pattern("nodes_expanded", r"Nodes expanded during search: (\d+)", type=int)
parser.add_pattern("nodes_pruned", r"Nodes pruned by bound: (\d+)", type=int)
parser.add_pattern("width_average", r"Average ef. width: (.+)", type=float)
parser.add_pattern("width_maximum", r"Max ef. width: (\d+)", type=int)
parser.add_function(error)
parser.add_function(coverage)
parser.add_function(adapt_average_effective_width)
parser.add_function(not_i_reachable)
parser.parse()