import dlplan

from ..instance_data.general_subproblem import GeneralSubproblemData
from ..instance_data.instance_data import InstanceData


class Policy:
    def __init__(self, policy: dlplan.Policy):
        self.policy = policy

    def solves(self, instance_data: InstanceData, general_subproblem_data: GeneralSubproblemData):
        evaluation_cache = dlplan.EvaluationCache(len(self.policy.get_boolean_features()), len(self.policy.get_numerical_features()))
        for root_idx, transitionss in general_subproblem_data.forward_transitions.items():
            root_context = dlplan.EvaluationContext(root_idx, instance_data.transition_system.states_by_index[root_idx], evaluation_cache)
            for transitions in transitionss:
                has_good_optimal_transitions = False
                for transition in transitions:
                    target_context = dlplan.EvaluationContext(transition.target_idx, instance_data.transition_system.states_by_index[transition.target_idx], evaluation_cache)
                    if self.policy.evaluate_lazy(root_context, target_context) is not None:
                        if transition.optimal:
                            has_good_optimal_transitions = True
                        else:
                            print("Suboptimal transition is marked as good: ", transition)
                            return False
                if not has_good_optimal_transitions:
                    print("Expanded state has no good optimal transition: ", root_idx)
                    return False
        return True
