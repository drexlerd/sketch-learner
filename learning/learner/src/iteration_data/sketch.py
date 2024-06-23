import math

from collections import defaultdict, deque
from termcolor import colored
from typing import Dict, List

from dlplan.core import State, DenotationsCaches
from dlplan.policy import Policy, NamedBoolean, NamedNumerical

from ..instance_data.instance_data import InstanceData, StateFinder
from ..domain_data.domain_data import DomainData


class Sketch:
    def __init__(self, dlplan_policy: Policy, width: int):
        self.dlplan_policy = dlplan_policy
        self.width = width

    def _verify_bounded_width(self, domain_data: DomainData, instance_datas: List[InstanceData], state_finder: StateFinder, instance_data: InstanceData, require_optimal_width=False):
        """
        Performs forward search over R-reachable states.
        Initially, the R-reachable states are all initial states.
        For each R-reachable state there must be a satisfied subgoal tuple.
        If optimal width is required, we do not allow R-compatible states
        that are closer than the closest satisfied subgoal tuple.
        """
        queue = deque()
        queue.extend(instance_data.initial_gfa_state_idxs)
        visited = set()
        visited.update(instance_data.initial_gfa_state_idxs)
        # byproduct for acyclicity check
        subgoal_states_per_r_reachable_state = defaultdict(set)
        while queue:
            gfa_root_idx = queue.pop()
            if instance_data.gfa.is_deadend_state(gfa_root_idx):
                print("Deadend state is r_reachable")
                print("State:", gfa_root_idx)
                return False, []
            if instance_data.gfa.is_goal_state(gfa_root_idx):
                continue

            gfa_root = instance_data.gfa.get_states()[gfa_root_idx]
            gfa_root_id = gfa_root.get_id()
            tuple_graph = domain_data.gfa_state_id_to_tuple_graph[gfa_root_id]

            new_instance_idx = domain_data.instance_idx_remap[gfa_root.get_abstraction_id()]
            dlplan_ss_root = state_finder.get_dlplan_ss_state(gfa_root)

            ḧas_bounded_width = False
            min_compatible_distance = math.inf
            for s_distance, tuple_vertex_idxs in enumerate(tuple_graph.get_vertex_indices_by_distances()):
                for mimir_ss_state_prime in tuple_graph.get_states_by_distance()[s_distance]:
                    gfa_state_prime = state_finder.get_gfa_state_from_ss_state_idx(new_instance_idx, instance_data.mimir_ss.get_state_index(mimir_ss_state_prime))
                    new_instance_prime_idx = domain_data.instance_idx_remap[gfa_state_prime.get_abstraction_id()]
                    instance_data_prime = instance_datas[new_instance_prime_idx]
                    gfa_state_prime_idx = instance_data_prime.gfa.get_state_index(gfa_state_prime)
                    dlplan_ss_state_prime = state_finder.get_dlplan_ss_state(gfa_state_prime)

                    if self.dlplan_policy.evaluate(dlplan_ss_root, dlplan_ss_state_prime, instance_data.denotations_caches) is not None:
                        min_compatible_distance = min(min_compatible_distance, s_distance)
                        subgoal_states_per_r_reachable_state[gfa_root_idx].add(gfa_state_prime_idx)
                        if gfa_state_prime_idx not in visited:
                            visited.add(gfa_state_prime_idx)
                            queue.append(gfa_state_prime_idx)

                # Check whether there exists a subgoal tuple for which all underlying states are subgoal states
                found_subgoal_tuple = False
                for tuple_vertex_idx in tuple_vertex_idxs:
                    tuple_vertex = tuple_graph.get_vertices()[tuple_vertex_idx]
                    is_subgoal_tuple = True
                    for mimir_ss_state_prime in tuple_vertex.get_states():
                        gfa_state_prime = state_finder.get_gfa_state_from_ss_state_idx(new_instance_idx, instance_data.mimir_ss.get_state_index(mimir_ss_state_prime))
                        new_instance_prime_idx = domain_data.instance_idx_remap[gfa_state_prime.get_abstraction_id()]
                        instance_data_prime = instance_datas[new_instance_prime_idx]
                        gfa_state_prime_idx = instance_data_prime.gfa.get_state_index(gfa_state_prime)
                        dlplan_ss_state_prime = state_finder.get_dlplan_ss_state(gfa_state_prime)

                        if self.dlplan_policy.evaluate(dlplan_ss_root, dlplan_ss_state_prime, instance_data.denotations_caches) is not None:
                            min_compatible_distance = min(min_compatible_distance, s_distance)
                            subgoal_states_per_r_reachable_state[gfa_root_idx].add(gfa_state_prime_idx)
                        else:
                            is_subgoal_tuple = False
                    if is_subgoal_tuple:
                        found_subgoal_tuple = True
                        break

                # Decide whether width is bounded or not
                if found_subgoal_tuple:
                    if require_optimal_width and min_compatible_distance < s_distance:
                        print(colored("Optimal width disproven.", "red", "on_grey"))
                        print("Min compatible distance:", min_compatible_distance)
                        print("Subgoal tuple distance:", s_distance)
                        return False, []
                    else:
                        ḧas_bounded_width = True
                        break

            if not ḧas_bounded_width:
                print(colored("Sketch fails to bound width of a state", "red", "on_grey"))
                print("Instance:", instance_data.idx)
                print("Source_state:", gfa_root_idx)
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
                    gfa_target_idx = next(iterator)
                    if instance_data.gfa.is_goal_state(gfa_target_idx):
                        continue
                    if gfa_target_idx in s_idxs_on_path:
                        print(colored("Sketch cycles", "red", "on_grey"))
                        print("Instance:", instance_data.idx)
                        for s_idx in s_idxs_on_path:
                            print(f"{s_idx}")
                        print(f"{gfa_target_idx}")
                        return False
                    if gfa_target_idx not in frontier:
                        frontier.add(gfa_target_idx)
                        stack.append((gfa_target_idx, iter(r_compatible_successors.get(gfa_target_idx, []))))
                except StopIteration:
                    s_idxs_on_path.discard(source_idx)
                    stack.pop(-1)
        return True

    def _compute_state_b_values(self, booleans: List[NamedBoolean], numericals: List[NamedNumerical], state: State, denotations_caches: DenotationsCaches):
        return tuple([boolean.get_element().evaluate(state, denotations_caches) for boolean in booleans] + [numerical.get_element().evaluate(state, denotations_caches) > 0 for numerical in numericals])

    def _verify_goal_separating_features(self, instance_data: InstanceData):
        """
        Returns True iff sketch features separate goal from nongoal states.
        """
        goal_b_values = set()
        nongoal_b_values = set()
        booleans = self.dlplan_policy.get_booleans()
        numericals = self.dlplan_policy.get_numericals()
        for s_idx, state in instance_data.state_space.get_states().items():
            b_values = self._compute_state_b_values(booleans, numericals, state, instance_data.denotations_caches)
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

    def solves(self, domain_data: DomainData, instance_datas: List[InstanceData], state_finder: StateFinder, instance_data: InstanceData, enable_goal_separating_features: bool):
        """
        Returns True iff the sketch solves the instance, i.e.,
            (1) subproblems have bounded width,
            (2) sketch only classifies delta optimal state pairs as good,
            (3) sketch is acyclic, and
            (4) sketch features separate goals from nongoal states. """
        bounded, subgoal_states_per_r_reachable_state = self._verify_bounded_width(domain_data, instance_datas, state_finder, instance_data)
        if not bounded:
            return False
        if enable_goal_separating_features:
            if not self._verify_goal_separating_features(instance_data):
                return False
        if not self._verify_acyclicity(instance_data, subgoal_states_per_r_reachable_state):
            return False
        return True

    def print(self):
        print(str(self.dlplan_policy))
        print("Numer of sketch rules:", len(self.dlplan_policy.get_rules()))
        print("Number of selected features:", len(self.dlplan_policy.get_booleans()) + len(self.dlplan_policy.get_numericals()))
        print("Maximum complexity of selected feature:", max([0] + [boolean.get_element().compute_complexity() for boolean in self.dlplan_policy.get_booleans()] + [numerical.get_element().compute_complexity() for numerical in self.dlplan_policy.get_numericals()]))
