import dlplan
import math

from termcolor import colored
from typing import Dict, List
from collections import defaultdict, deque

from learner.src.instance_data.instance_data import InstanceData


class Sketch:
    def __init__(self, booleans: List[dlplan.Boolean], numericals: List[dlplan.Numerical], dlplan_policy: dlplan.Policy, width: int):
        self.booleans = booleans
        self.numericals = numericals
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
        queue.extend(instance_data.initial_s_idxs)
        visited = set()
        visited.update(instance_data.initial_s_idxs)
        # byproduct for acyclicity check
        subgoal_states_per_r_reachable_state = defaultdict(set)
        while queue:
            root_idx = queue.pop()
            if instance_data.is_deadend(root_idx):
                print("Deadend state is r_reachable")
                print("State:", instance_data.state_space.get_states()[root_idx])
                return False, []
            if instance_data.is_goal(root_idx):
                continue
            tuple_graph = instance_data.tuple_graphs[root_idx]
            source_state = instance_data.state_space.get_states()[root_idx]
            bounded = False
            min_compatible_distance = math.inf
            for tuple_distance, tuple_nodes in enumerate(tuple_graph.get_tuple_nodes_by_distance()):
                for tuple_node in tuple_nodes:
                    subgoal = True
                    for s_prime_idx in tuple_node.get_state_indices():
                        target_state = instance_data.state_space.get_states()[s_prime_idx]
                        if self.dlplan_policy.evaluate_lazy(source_state, target_state, instance_data.denotations_caches) is not None:
                            min_compatible_distance = min(min_compatible_distance, tuple_distance)
                            subgoal_states_per_r_reachable_state[root_idx].add(s_prime_idx)
                            if s_prime_idx not in visited:
                                visited.add(s_prime_idx)
                                queue.append(s_prime_idx)
                        else:
                            subgoal = False
                    if subgoal:
                        if require_optimal_width and min_compatible_distance < tuple_distance:
                            print(colored("Optimal width disproven.", "red", "on_grey"))
                            print("Min compatible distance:", min_compatible_distance)
                            print("Subgoal tuple distance:", tuple_distance)
                            return False, []
                        bounded = True
                if bounded:
                    break
            if not bounded:
                print(colored("Sketch fails to bound width of a state", "red", "on_grey"))
                print("Instance:", instance_data.id, instance_data.instance_information.name)
                print("Source_state:", source_state.get_index(), str(source_state))
                return False, []
        return True, subgoal_states_per_r_reachable_state

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
                    if instance_data.is_goal(target_idx):
                        continue
                    if target_idx in s_idxs_on_path:
                        print(colored("Sketch cycles", "red", "on_grey"))
                        print("Instance:", instance_data.id, instance_data.instance_information.name)
                        for s_idx in s_idxs_on_path:
                            print(f"{s_idx} {str(instance_data.state_space.get_states()[s_idx])}")
                        print(f"{target_idx} {str(instance_data.state_space.get_states()[target_idx])}")
                        return False
                    if target_idx not in frontier:
                        frontier.add(target_idx)
                        stack.append((target_idx, iter(r_compatible_successors.get(target_idx, []))))
                except StopIteration:
                    s_idxs_on_path.discard(source_idx)
                    stack.pop(-1)
        return True

    def _compute_state_b_values(self, booleans: List[dlplan.Boolean], numericals: List[dlplan.Numerical], instance_data: InstanceData, state: dlplan.State):
        return tuple([boolean.evaluate(state, instance_data.denotations_caches) for boolean in booleans] + [numerical.evaluate(state, instance_data.denotations_caches) > 0 for numerical in numericals])

    def _verify_goal_separating_features(self, instance_data: InstanceData):
        """
        Returns True iff sketch features separate goal from nongoal states.
        """
        goal_b_values = set()
        nongoal_b_values = set()
        for s_idx, state in instance_data.state_space.get_states().items():
            b_values = self._compute_state_b_values(self.booleans, self.numericals, instance_data, state)
            separating = True
            if instance_data.is_goal(s_idx):
                goal_b_values.add(b_values)
                if b_values in nongoal_b_values:
                    separating = False
            else:
                nongoal_b_values.add(b_values)
                if b_values in goal_b_values:
                    separating = False
            if not separating:
                print("Features do not separate goals from non goals")
                print("Booleans:")
                print("State:", str(state))
                print("b_values:", b_values)
                return False
        return True

    def solves(self, config, instance_data: InstanceData):
        """
        Returns True iff the sketch solves the instance, i.e.,
            (1) subproblems have bounded width,
            (2) sketch only classifies delta optimal state pairs as good,
            (3) sketch is acyclic, and
            (4) sketch features separate goals from nongoal states. """
        bounded, subgoal_states_per_r_reachable_state = self._verify_bounded_width(instance_data)
        if not bounded:
            return False
        if config.goal_separation:
            if not self._verify_goal_separating_features(instance_data):
                return False
        if not self._verify_acyclicity(instance_data, subgoal_states_per_r_reachable_state):
            return False
        return True

    def print(self):
        print(self.dlplan_policy.str())
        print("Numer of sketch rules:", len(self.dlplan_policy.get_rules()))
        print("Number of selected features:", len(self.booleans) + len(self.numericals))
        print("Maximum complexity of selected feature:", max([0] + [boolean.compute_complexity() for boolean in self.booleans] + [numerical.compute_complexity() for numerical in self.numericals]))
