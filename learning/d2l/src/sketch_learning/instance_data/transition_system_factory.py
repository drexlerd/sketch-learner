import math

from collections import defaultdict, deque
from typing import List


from .state_pair_classifier import StatePairClassifier
from .transition_system import TransitionSystem
from .transition_system_utils import compute_deadends, compute_goal_distances, compute_inverse_transitions


class TransitionSystemFactory:
    def make_transition_system(self, s_idx_to_dlplan_state, goals, forward_transitions, initial_s_idx=0):
        # Compute backward transitions and deadends
        backward_transitions = compute_inverse_transitions(forward_transitions)
        goal_distances = compute_goal_distances(s_idx_to_dlplan_state, goals, backward_transitions)
        deadends = compute_deadends(goal_distances)
        return TransitionSystem(initial_s_idx, s_idx_to_dlplan_state, forward_transitions, backward_transitions, deadends, goals)
