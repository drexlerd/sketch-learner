import logging
from .facts.alive import Alive
from .facts.initial import Initial
from .facts.goal import Goal
from .facts.nongoal import NonGoal
from .facts.solvable import Solvable
from .facts.unsolvable import Unsolvable
from .facts.state_distance import StateDistance
from .facts.exceed import Exceed
from .facts.tuple import Tuple
from .facts.tuple_distance import TupleDistance
from .facts.contain import Contain
from .facts.feature import Feature
from .facts.boolean_feature import BooleanFeature
from .facts.numerical_feature import NumericalFeature
from .facts.boolean_feature_valuation import BooleanFeatureValuation
from .facts.numerical_feature_valuation import NumericalFeatureValuation
from .facts.feature_complexity import FeatureComplexity


class ASPInstanceBuilder:
    """ Builder for the instance file of an ASP containing facts. """
    def __init__(self):
        # transition system
        self.initials = [] # deprecated
        self.alives = []
        self.goals = []  # deprecated
        self.nongoals = []  # deprecated
        self.solvables = []
        self.unsolvables = []
        # finite pairwise distances
        self.state_distances = []
        # tuple graph
        self.exceeds = []
        self.tuples = []
        self.tuple_distances = []
        self.contains = []
        # features
        self.features = []
        self.boolean_features = []
        self.numerical_features = []
        self.boolean_feature_valuations = []
        self.numerical_feature_valuations = []
        self.feature_complexities = []

        # The total number of facts added
        self.num_facts = 0

    def add_initial(self, instance_idx, s_idx):
        self.initials.append(Initial(instance_idx, s_idx))
        self.num_facts += 1

    def add_alive(self, instance_idx, s_idx):
        self.alives.append(Alive(instance_idx, s_idx))
        self.num_facts += 1

    def add_goal(self, instance_idx, s_idx):
        self.goals.append(Goal(instance_idx, s_idx))
        self.num_facts += 1

    def add_nongoal(self, instance_idx, s_idx):
        self.nongoals.append(NonGoal(instance_idx, s_idx))
        self.num_facts += 1

    def add_solvable(self, instance_idx, s_idx):
        self.solvables.append(Solvable(instance_idx, s_idx))
        self.num_facts += 1

    def add_unsolvable(self, instance_idx, s_idx):
        self.unsolvables.append(Unsolvable(instance_idx, s_idx))
        self.num_facts += 1

    def add_state_distance(self, instance_idx, source_idx, target_idx, distance):
        self.state_distances.append(StateDistance(instance_idx, source_idx, target_idx, distance))
        self.num_facts += 1

    def add_exceed(self, instance_idx, s_idx):
        self.exceeds.append(Exceed(instance_idx, s_idx))
        self.num_facts += 1

    def add_tuple(self, instance_idx, root_idx, t_idx):
        self.tuples.append(Tuple(instance_idx, root_idx, t_idx))
        self.num_facts += 1

    def add_tuple_distance(self, instance_idx, root_idx, t_idx, distance):
        self.tuple_distances.append(TupleDistance(instance_idx, root_idx, t_idx, distance))
        self.num_facts += 1

    def add_contain(self, instance_idx, root_idx, s_idx, t_idx):
        self.contains.append(Contain(instance_idx, root_idx, s_idx, t_idx))
        self.num_facts += 1

    def add_boolean_feature(self, f_idx, complexity):
        self.features.append(Feature(f_idx))
        self.boolean_features.append(BooleanFeature(f_idx))
        self.feature_complexities.append(FeatureComplexity(f_idx, complexity))
        self.num_facts += 1

    def add_numerical_feature(self, f_idx, complexity):
        self.features.append(Feature(f_idx))
        self.numerical_features.append(NumericalFeature(f_idx))
        self.feature_complexities.append(FeatureComplexity(f_idx, complexity))
        self.num_facts += 1

    def add_boolean_feature_valuation(self, instance_idx, f_idx, s_idx, f_valuation):
        self.boolean_feature_valuations.append(BooleanFeatureValuation(instance_idx, f_idx, s_idx, f_valuation))
        self.num_facts += 1

    def add_numerical_feature_valuation(self, instance_idx, f_idx, s_idx, f_valuation):
        self.numerical_feature_valuations.append(NumericalFeatureValuation(instance_idx, f_idx, s_idx, f_valuation))
        self.num_facts += 1

    def log_stats(self):
        logging.info(f"Generated {self.num_facts} facts:\n\
solvables: {len(self.solvables)}\n\
unsolvables: {len(self.unsolvables)}\n\
exceeds: {len(self.exceeds)}\n\
state_distances: {len(self.state_distances)}\n\
tuples: {len(self.tuples)}\n\
tuple_distances: {len(self.tuple_distances)}\n\
contains: {len(self.contains)}\n\
features: {len(self.features)}\n\
boolean_features: {len(self.boolean_features)}\n\
numerical_features: {len(self.numerical_features)}\n\
feature_complexity: {len(self.feature_complexities)}\n\
boolean_feature_valuations: {len(self.boolean_feature_valuations)}\n\
numerical_feature_valuations: {len(self.numerical_feature_valuations)}")

    def __str__(self):
        return "".join([str(initial) for initial in self.initials]) + \
               "".join([str(alive) for alive in self.alives]) + \
               "".join([str(goal) for goal in self.goals]) + \
               "".join([str(nongoal) for nongoal in self.nongoals]) + \
               "".join([str(solvable) for solvable in self.solvables]) + \
               "".join([str(unsolvable) for unsolvable in self.unsolvables]) + \
               "".join([str(exceed) for exceed in self.exceeds]) + \
               "".join([str(state_distance) for state_distance in self.state_distances]) + \
               "".join([str(tuple) for tuple in self.tuples]) + \
               "".join([str(tuple_distance) for tuple_distance in self.tuple_distances]) + \
               "".join([str(contain) for contain in self.contains]) + \
               "".join([str(feature) for feature in self.features]) + \
               "".join([str(boolean_feature) for boolean_feature in self.boolean_features]) + \
               "".join([str(numerical_feature) for numerical_feature in self.numerical_features]) + \
               "".join([str(feature_complexity) for feature_complexity in self.feature_complexities]) + \
               "".join([str(feature_valuation) for feature_valuation in self.boolean_feature_valuations]) + \
               "".join([str(feature_valuation) for feature_valuation in self.numerical_feature_valuations])
