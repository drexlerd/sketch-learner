import dlplan

from ..instance_data.instance_data import InstanceData
from ..instance_data.state_pair_classifier import StatePairClassifier, StatePairClassification


class Policy:
    def __init__(self, dlplan_policy: dlplan.Policy):
        self.dlplan_policy = dlplan_policy

    def solves(self, instance_data: InstanceData, state_pair_classifier: StatePairClassifier):
        evaluation_cache = dlplan.EvaluationCache(len(self.dlplan_policy.get_boolean_features()), len(self.dlplan_policy.get_numerical_features()))
        for source_idx, state_pairs in state_pair_classifier.source_idx_to_state_pairs.items():
            root_dlplan_state = instance_data.transition_system.s_idx_to_dlplan_state[source_idx]
            root_context = dlplan.EvaluationContext(source_idx, instance_data.transition_system.s_idx_to_dlplan_state[source_idx], evaluation_cache)
            has_good_optimal_transitions = False
            for state_pair in state_pairs:
                target_dlplan_state = instance_data.transition_system.s_idx_to_dlplan_state[state_pair.target_idx]
                target_context = dlplan.EvaluationContext(state_pair.target_idx, target_dlplan_state, evaluation_cache)
                if self.dlplan_policy.evaluate_lazy(root_context, target_context) is not None:
                    classification = state_pair_classifier.classify(state_pair)
                    if classification == StatePairClassification.DELTA_OPTIMAL:
                        has_good_optimal_transitions = True
                    elif classification == StatePairClassification.NOT_DELTA_OPTIMAL:
                        print(instance_data.instance_information.instance_filename)
                        print("Suboptimal transition is marked as good: ", str(root_dlplan_state), "->", str(target_dlplan_state))
                        return False
                    else:
                        raise Exception("Policy::solves - unknown StatePairClassification", classification)
            if not has_good_optimal_transitions:
                print(instance_data.instance_information.instance_filename)
                print("Expanded state has no good optimal transition: ", str(root_dlplan_state))
                return False
        return True

    def compute_unsatisfied_d2_facts(self):
        """ TODO: we want to incrementally add D2 constraints. """
        pass
