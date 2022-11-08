import dlplan
import math
from termcolor import colored
from typing import Dict, MutableSet
from collections import defaultdict, deque

from ..instance_data.state_pair import StatePair
from ..instance_data.instance_data import InstanceData


class Sketch:
    def __init__(self, dlplan_policy: dlplan.Policy, width: int):
        self.dlplan_policy = dlplan_policy
        self.width = width

    def _verify_bounded_width(self, instance_data: InstanceData, require_optimal_width=False):
        """
        Performs forward search over R-reachable states.
        Initially, the R-reachable states are all initial states.
        For each R-reachable state there must be a satisfied subgoal tuple.
        If optimal width is required, we do not allow R-compatible states
        that are closer than the closest satisfied subgoal tuple.
        """
        queue = deque()
        r_reachable_states = set()
        r_compatible_successors = defaultdict(set)
        for initial_s_idx in instance_data.initial_s_idxs:
            queue.append(initial_s_idx)
            r_reachable_states.add(initial_s_idx)
        while queue:
            s_idx = queue.pop()
            if instance_data.goal_distance_information.is_goal(s_idx):
                continue
            tuple_graph = instance_data.tuple_graphs[s_idx]
            source_state = instance_data.state_information.get_state(s_idx)
            bounded = False
            min_compatible_distance = math.inf
            for tuple_distance, tuple_nodes in enumerate(tuple_graph.get_tuple_nodes_by_distance()):
                for tuple_node in tuple_nodes:
                    subgoal = True
                    for s_prime_idx in tuple_node.get_state_indices():
                        target_state = instance_data.state_information.get_state(s_prime_idx)
                        #print(source_state, "->", target_state, ":", self.dlplan_policy.evaluate_lazy(source_state, target_state, instance_data.denotations_caches))
                        #print([numerical.evaluate(source_state) for numerical in self.dlplan_policy.get_numerical_features()])
                        #print([numerical.evaluate(target_state) for numerical in self.dlplan_policy.get_numerical_features()])
                        if self.dlplan_policy.evaluate_lazy(source_state, target_state, instance_data.denotations_caches) is not None:
                            if instance_data.goal_distance_information.is_deadend(s_prime_idx):
                                print(colored(f"Sketch leads to an unsolvable state.", "red", "on_grey"))
                                print("Instance:", instance_data.id, instance_data.instance_information.name)
                                print("Target_state:", source_state.get_index(), str(source_state))
                                print("Target_state:", target_state.get_index(), str(target_state))
                                return [], False
                            min_compatible_distance = min(min_compatible_distance, tuple_distance)
                            r_compatible_successors[s_idx].add(s_prime_idx)
                            if s_prime_idx not in r_reachable_states:
                                r_reachable_states.add(s_prime_idx)
                                queue.append(s_prime_idx)
                        else:
                            subgoal = False
                    if subgoal:
                        if require_optimal_width and min_compatible_distance < tuple_distance:
                            print(colored(f"Optimal width disproven.", "red", "on_grey"))
                            print("Min compatible distance:", min_compatible_distance)
                            print("Subgoal tuple distance:", tuple_distance)
                            return [], False
                        bounded = True
                if bounded:
                    break
            if not bounded:
                print(colored(f"Sketch fails to bound width of a state", "red", "on_grey"))
                print("Instance:", instance_data.id, instance_data.instance_information.name)
                print("Source_state:", source_state.get_index(), str(source_state))
                return [], False
        return r_compatible_successors, True

    def _verify_acyclicity(self, instance_data: InstanceData, r_compatible_successors: Dict[int, int]):
        """
        Returns True iff sketch is acyclic, i.e., no infinite trajectories s1,s2,... are possible.
        """
        for s_idx, successors in r_compatible_successors.items():
            # The depth-first search is the iterative version where the current path is explicit in the stack.
            # https://en.wikipedia.org/wiki/Depth-first_search
            stack = [(s_idx, iter(successors))]
            s_idxs_on_path = {s_idx,}
            frontier = set()  # the generated states, to ensure that they are only added once to the stack
            while stack:
                source_idx, iterator = stack[-1]
                s_idxs_on_path.add(source_idx)
                try:
                    target_idx = next(iterator)
                    if instance_data.goal_distance_information.is_goal(target_idx):
                        continue
                    if target_idx in s_idxs_on_path:
                        print(colored("Sketch cycles", "red", "on_grey"))
                        print("Instance:", instance_data.id, instance_data.instance_information.name)
                        for s_idx in s_idxs_on_path:
                            print(f"{s_idx} {str(instance_data.state_information.get_state(s_idx))}")
                        print(f"{target_idx} {str(instance_data.state_information.get_state(target_idx))}")
                        return False
                    if target_idx not in frontier:
                        frontier.add(target_idx)
                        stack.append((target_idx, iter(r_compatible_successors.get(target_idx, []))))
                except StopIteration:
                    s_idxs_on_path.discard(source_idx)
                    stack.pop(-1)
        return True

    def _verify_goal_separating_features(self, instance_data: InstanceData):
        """
        Returns True iff sketch features separate goal from nongoal states.
        """
        dlplan_policy_features = self.dlplan_policy.get_boolean_features() + self.dlplan_policy.get_numerical_features()
        s_idx_to_feature_valuations = dict()
        for s_idx in instance_data.state_space.get_state_indices():
            s_idx_to_feature_valuations[s_idx] = tuple([feature.evaluate(instance_data.state_information.get_state(s_idx)) for feature in dlplan_policy_features])
        for s_idx_1 in instance_data.state_space.get_state_indices():
            for s_idx_2 in instance_data.state_space.get_state_indices():
                if (instance_data.goal_distance_information.is_goal(s_idx_1) and \
                    not instance_data.goal_distance_information.is_goal(s_idx_2)):
                    if (s_idx_to_feature_valuations[s_idx_1] == s_idx_to_feature_valuations[s_idx_2]):
                        print(colored("Selected features do not separate goals from non goals.", "red", "on_grey"))
                        print("Instance:", instance_data.id, instance_data.instance_information.name)
                        print("Goal state:", s_idx_1, str(instance_data.state_information.get_state(s_idx_1)), s_idx_to_feature_valuations[s_idx_1])
                        print("Nongoal state:", s_idx_2, str(instance_data.state_information.get_state(s_idx_2)), s_idx_to_feature_valuations[s_idx_2])
                        return False
        return True

    def solves(self, config, instance_data: InstanceData):
        """
        Returns True iff the sketch solves the instance, i.e.,
            (1) subproblems have bounded width,
            (2) sketch only classifies delta optimal state pairs as good,
            (3) sketch is acyclic, and
            (4) sketch features separate goals from nongoal states. """
        r_compatible_successors, bounded_width = self._verify_bounded_width(instance_data)
        if not bounded_width:
            return False
        if config.goal_separation:
            if not self._verify_goal_separating_features(instance_data):
                return False
        if not self._verify_acyclicity(instance_data, r_compatible_successors):
            return False
        return True

    def print(self):
        print(self.dlplan_policy.compute_repr())
        print("Numer of sketch rules:", len(self.dlplan_policy.get_rules()))
        print("Number of selected features:", len(self.dlplan_policy.get_boolean_features()) + len(self.dlplan_policy.get_numerical_features()))
        print("Maximum complexity of selected feature:", max([0] + [boolean_feature.compute_complexity() for boolean_feature in self.dlplan_policy.get_boolean_features()] + [numerical_feature.compute_complexity() for numerical_feature in self.dlplan_policy.get_numerical_features()]))
