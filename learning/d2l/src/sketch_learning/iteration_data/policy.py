import dlplan

from ..instance_data.subproblem import Subproblem
from ..instance_data.instance_data import InstanceData


class Policy:
    def __init__(self, dlplan_policy: dlplan.Policy):
        self.dlplan_policy = dlplan_policy

    def solves(self, subproblem_data: Subproblem, instance_data: InstanceData):
        evaluation_cache = dlplan.EvaluationCache(len(self.dlplan_policy.get_boolean_features()), len(self.dlplan_policy.get_numerical_features()))
        for root_idx, transitions in subproblem_data.forward_transitions.items():
            root_dlplan_state = instance_data.transition_system.s_idx_to_dlplan_state[root_idx]
            root_context = dlplan.EvaluationContext(root_idx, instance_data.transition_system.s_idx_to_dlplan_state[root_idx], evaluation_cache)
            has_good_optimal_transitions = False
            for transition in transitions:
                target_dlplan_state = instance_data.transition_system.s_idx_to_dlplan_state[transition.target_idx]
                target_context = dlplan.EvaluationContext(transition.target_idx, target_dlplan_state, evaluation_cache)
                if self.dlplan_policy.evaluate_lazy(root_context, target_context) is not None:
                    if transition.optimal:
                        has_good_optimal_transitions = True
                    else:
                        print(instance_data.instance_information.instance_filename)
                        print("Suboptimal transition is marked as good: ", str(root_dlplan_state), "->", str(target_dlplan_state))
                        return False
            if not has_good_optimal_transitions:
                print(instance_data.instance_information.instance_filename)
                print("Expanded state has no good optimal transition: ", str(root_dlplan_state))
                return False
        return True
