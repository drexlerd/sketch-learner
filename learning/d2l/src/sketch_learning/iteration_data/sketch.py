import dlplan
from termcolor import colored
from typing import Dict, MutableSet
from collections import defaultdict, deque

from ..instance_data.state_pair import StatePair
from ..instance_data.instance_data import InstanceData


class Sketch:
    def __init__(self, dlplan_policy: dlplan.Policy, width: int):
        self.dlplan_policy = dlplan_policy
        self.width = width

    def _verify_bounded_width_2(self, instance_data: InstanceData):
        """
        """
        for initial_s_idx in instance_data.initial_s_idxs:
            r_reachable_states = set()
            r_reachable_states.add(initial_s_idx)
            queue = deque()
            queue.append(initial_s_idx)
            top_goal_achieved = False
            while queue:
                s_idx = queue.pop()
                tuple_graph = instance_data.tuple_graphs[s_idx]
                source_state = instance_data.state_information.get_state(s_idx)
                bounded = False
                for tuple_nodes in tuple_graph.get_tuple_nodes_by_distance():
                    for tuple_node in tuple_nodes:
                        t_idx = tuple_node.get_tuple_index()
                        subgoal = True
                        for s_prime_idx in tuple_node.get_state_indices():
                            target_state = instance_data.state_information.get_state(s_prime_idx)
                            if self.dlplan_policy.evaluate_lazy(source_state, target_state, instance_data.denotations_caches) is not None:
                                if s_prime_idx not in r_reachable_states:
                                    r_reachable_states.add(s_prime_idx)
                                    queue.append(s_prime_idx)
                                if instance_data.goal_distance_information.is_deadend(s_prime_idx):
                                    print(colored(f"Sketch leads to an unsolvable state.", "red", "on_grey"))
                                    print("Instance:", instance_data.id, instance_data.instance_information.name)
                                    print("Target_state:", target_state.get_index(), str(target_state))
                                    return False
                            else:
                                subgoal = False
                        if subgoal:
                            tuple_achieves_top_goal = True
                            for s_prime_idx in tuple_node.get_state_indices():
                                if not instance_data.goal_distance_information.is_goal(s_prime_idx):
                                    tuple_achieves_top_goal = False
                            if tuple_achieves_top_goal:
                                top_goal_achieved = True
                            bounded = True
                    if bounded:
                        break
            if not top_goal_achieved:
                print(colored(f"Sketch does not achieve top goal.", "red", "on_grey"))
                print(str(instance_data.state_information.get_state(instance_data.state_space.get_initial_state_index())))
                return False
        return True


    def _verify_bounded_width(self, instance_data: InstanceData):
        """
        Returns three parts:
            (1) the closest subgoal states for every alive state,
            (2) the closest subgoal tuples for every alive state, and
            (3) True if the width of every alive state is bounded.
        """
        root_idx_to_closest_subgoal_s_idxs = defaultdict(set)
        root_idx_to_closest_subgoal_t_idxs = defaultdict(set)
        for root_idx, tuple_graph in instance_data.tuple_graphs.items():
            bounded = False
            source_state = instance_data.state_information.get_state(root_idx)
            for tuple_nodes in tuple_graph.get_tuple_nodes_by_distance():
                for tuple_node in tuple_nodes:
                    t_idx = tuple_node.get_tuple_index()
                    subgoal = True
                    assert tuple_node.get_state_indices()
                    for s_idx in tuple_node.get_state_indices():
                        target_state = instance_data.state_information.get_state(s_idx)
                        if self.dlplan_policy.evaluate_lazy(source_state, target_state, instance_data.denotations_caches) is not None:
                            root_idx_to_closest_subgoal_s_idxs[tuple_graph.get_root_state_index()].add(s_idx)
                            if instance_data.goal_distance_information.is_deadend(s_idx):
                                print(colored(f"Sketch leads to an unsolvable state", "red", "on_grey"))
                                print("Instance:", instance_data.id, instance_data.instance_information.name)
                                print("Target_state:", target_state.get_index(), str(target_state))
                                return [], [], False
                        else:
                            subgoal = False
                    if subgoal:
                        root_idx_to_closest_subgoal_t_idxs[tuple_graph.get_root_state_index()].add(t_idx)
                        bounded = True
                if bounded:
                    break
            if not bounded:
                print(colored(f"Sketch fails to bound width of a state", "red", "on_grey"))
                print("Instance:", instance_data.id, instance_data.instance_information.name)
                print("Source_state:", source_state.get_index(), str(source_state))
                return [], [], False
        return root_idx_to_closest_subgoal_s_idxs, root_idx_to_closest_subgoal_t_idxs, True

    def _verify_acyclicity(self, instance_data: InstanceData):
        """
        Returns True iff sketch is acyclic, i.e., no infinite trajectories s1,s2,... are possible.
        """
        features = self.dlplan_policy.get_boolean_features() + self.dlplan_policy.get_numerical_features()
        state_information = instance_data.state_information
        # 1. Compute feature valuations F over Phi for each state
        feature_valuation_to_s_idxs = defaultdict(set)
        for s_idx in instance_data.state_space.get_state_indices():
            feature_valuation = tuple([feature.evaluate(state_information.get_state(s_idx)) for feature in features])
            feature_valuation_to_s_idxs[feature_valuation].add(s_idx)


        for root_idx in range(instance_data.state_space.get_num_states()):
            # The depth-first search is the iterative version where the current path is explicit in the stack.
            # https://en.wikipedia.org/wiki/Depth-first_search
            stack = [(root_idx, iter(root_idx_to_closest_subgoal_s_idxs[root_idx]))]
            s_idxs_on_path = {root_idx,}
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
                        stack.append((target_idx, iter(root_idx_to_closest_subgoal_s_idxs[target_idx])))
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
        if not self._verify_bounded_width_2(instance_data):
            return False
        if config.goal_separation:
            if not self._verify_goal_separating_features(instance_data):
                return False
        if not self._verify_acyclicity(instance_data):
            return False
        return True

    def print(self):
        print(self.dlplan_policy.compute_repr())
        print("Numer of sketch rules:", len(self.dlplan_policy.get_rules()))
        print("Number of selected features:", len(self.dlplan_policy.get_boolean_features()) + len(self.dlplan_policy.get_numerical_features()))
        print("Maximum complexity of selected feature:", max([0] + [boolean_feature.compute_complexity() for boolean_feature in self.dlplan_policy.get_boolean_features()] + [numerical_feature.compute_complexity() for numerical_feature in self.dlplan_policy.get_numerical_features()]))
