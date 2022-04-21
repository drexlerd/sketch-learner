import logging
from .facts.feature_data.boolean import Boolean
from .facts.feature_data.complexity import Complexity
from .facts.feature_data.feature import Feature
from .facts.feature_data.numerical import Numerical
from .facts.rules.conditions import C_EQ, C_GT, C_NEG, C_POS
from .facts.rules.effects import E_BOT, E_DEC, E_INC, E_NEG, E_POS
from .facts.termination_graph.termination_edge import TerminationEdge
from .facts.termination_graph.termination_node import TerminationNode
from .facts.termination_graph.termination_loop import TerminationLoop
from .facts.termination_graph.solvable import Solvable
from .facts.termination_graph.contains import EquivalenceContains
from .facts.tuple_graph.contain import Contain
from .facts.tuple_graph.deadend_distance import DeadendDistance
from .facts.tuple_graph.equivalence import Equivalence
from .facts.tuple_graph.exceed import Exceed
from .facts.tuple_graph.tuple import Tuple
from .facts.tuple_graph.tuple_distance import TupleDistance


class ASPInstanceBuilder:
    """ Builder for the instance file of an ASP containing facts. """
    def __init__(self):
        # feature facts
        self.features = []
        self.booleans = []
        self.numericals = []
        self.complexities = []
        # rules facts
        self.conditions = []
        self.effects = []
        # termination graph facts
        self.termination_nodes = []
        self.termination_loops = []
        self.termination_edges = []
        self.solvables = []
        self.equivalence_contains = []
        # tuple graph facts
        self.exceeds = []
        self.tuples = []
        self.equivalences = []
        self.contains = []
        self.t_distances = []
        self.d_distances = []
        # The total number of facts added
        self.num_facts = 0

    def add_boolean_feature(self, f_idx, complexity):
        self.features.append(Feature(f_idx))
        self.booleans.append(Boolean(f_idx))
        self.complexities.append(Complexity(f_idx, complexity))
        self.num_facts += 3

    def add_numerical_feature(self, f_idx, complexity):
        self.features.append(Feature(f_idx))
        self.numericals.append(Numerical(f_idx))
        self.complexities.append(Complexity(f_idx, complexity))
        self.num_facts += 3

    def add_c_eq(self, r_idx, f_idx):
        self.conditions.append(C_EQ(r_idx, f_idx))
        self.num_facts += 1

    def add_c_gt(self, r_idx, f_idx):
        self.conditions.append(C_GT(r_idx, f_idx))
        self.num_facts += 1

    def add_c_pos(self, r_idx, f_idx):
        self.conditions.append(C_POS(r_idx, f_idx))
        self.num_facts += 1

    def add_c_neg(self, r_idx, f_idx):
        self.conditions.append(C_NEG(r_idx, f_idx))
        self.num_facts += 1

    def add_e_inc(self, r_idx, f_idx):
        self.effects.append(E_INC(r_idx, f_idx))
        self.num_facts += 1

    def add_e_dec(self, r_idx, f_idx):
        self.effects.append(E_DEC(r_idx, f_idx))
        self.num_facts += 1

    def add_e_pos(self, r_idx, f_idx):
        self.effects.append(E_POS(r_idx, f_idx))
        self.num_facts += 1

    def add_e_neg(self, r_idx, f_idx):
        self.effects.append(E_NEG(r_idx, f_idx))
        self.num_facts += 1

    def add_e_bot(self, r_idx, f_idx):
        self.effects.append(E_BOT(r_idx, f_idx))
        self.num_facts += 1

    def add_termination_node(self, instance_idx, r_idx):
        self.termination_nodes.append(TerminationNode(instance_idx, r_idx))
        self.num_facts += 1

    def add_termination_loop(self, instance_idx, r_idx):
        self.termination_loops.append(TerminationLoop(r_idx))
        self.num_facts += 1

    def add_termination_edge(self, instance_idx, r_idx_source, r_idx_target):
        self.termination_edges.append(TerminationEdge(instance_idx, r_idx_source, r_idx_target))
        self.num_facts += 1

    def add_solvable(self, instance_idx, s_idx):
        self.solvables.append(Solvable(instance_idx, s_idx))
        self.num_facts += 1

    def add_equivalence_contains(self, instance_idx, r_idx, s_idx_from, s_idx_to):
        self.equivalence_contains.append(EquivalenceContains(instance_idx, r_idx, s_idx_from, s_idx_to))
        self.num_facts += 1

    def add_exceed(self, instance_idx, s_idx):
        self.exceeds.append(Exceed(instance_idx, s_idx))
        self.num_facts += 1

    def add_tuple(self, instance_idx, root_idx, t_idx):
        self.tuples.append(Tuple(instance_idx, root_idx, t_idx))
        self.num_facts += 1

    def add_equivalence(self, r_idx):
        self.equivalences.append(Equivalence(r_idx))
        self.num_facts += 1

    def add_contain(self, instance_idx, root_idx, t_idx, r_idx):
        self.contains.append(Contain(instance_idx, root_idx, t_idx, r_idx))
        self.num_facts += 1

    def add_tuple_distance(self, instance_idx, root_idx, t_idx, distance):
        self.t_distances.append(TupleDistance(instance_idx, root_idx, t_idx, distance))
        self.num_facts += 1

    def add_deadend_distance(self, instance_idx, root_idx, r_idx, distance):
        self.d_distances.append(DeadendDistance(instance_idx, root_idx, r_idx, distance))
        self.num_facts += 1


    def log_stats(self):
        logging.info(f"Generated {self.num_facts} facts:\n\
features: {len(self.features)}\n\
booleans: {len(self.booleans)}\n\
numericals: {len(self.numericals)}\n\
complexities: {len(self.complexities)}\n\
conditions: {len(self.conditions)}\n\
effects: {len(self.effects)}\n\
solvables: {len(self.solvables)}\n\
equivalence_contains: {len(self.equivalence_contains)}\n\
exceeds: {len(self.exceeds)}\n\
tuples: {len(self.tuples)}\n\
equivalences: {len(self.equivalences)}\n\
contains: {len(self.contains)}\n\
t_distances: {len(self.t_distances)}\n\
d_distances: {len(self.d_distances)}")

    def __str__(self):
        return "".join([str(x) for x in self.features]) + \
               "".join([str(x) for x in self.booleans]) + \
               "".join([str(x) for x in self.numericals]) + \
               "".join([str(x) for x in self.complexities]) + \
               "".join([str(x) for x in self.conditions]) + \
               "".join([str(x) for x in self.effects]) + \
               "".join([str(x) for x in self.solvables]) + \
               "".join([str(x) for x in self.equivalence_contains]) + \
               "".join([str(x) for x in self.exceeds]) + \
               "".join([str(x) for x in self.tuples]) + \
               "".join([str(x) for x in self.equivalences]) + \
               "".join([str(x) for x in self.contains]) + \
               "".join([str(x) for x in self.t_distances]) + \
               "".join([str(x) for x in self.d_distances])
