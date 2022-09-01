from clingo import Number

from ....instance_data.state_pair_classifier import StatePairClassifier, StatePairClassification
from ....instance_data.transition_system import TransitionSystem
from ....iteration_data.instance_feature_data import InstanceFeatureData


class TransitionSystemFactFactory():
    def make_facts(self, instance_idx: int, transition_system: TransitionSystem, state_pair_classifier: StatePairClassifier):
        facts = []
        for s_idx in state_pair_classifier.generated_s_idxs:
            if not transition_system.is_deadend(s_idx):
                facts.append(("solvable", [Number(instance_idx), Number(s_idx)]))
            if transition_system.is_goal(s_idx):
                facts.append(("goal", [Number(instance_idx), Number(s_idx)]))
            else:
                facts.append(("nongoal", [Number(instance_idx), Number(s_idx)]))
            if transition_system.is_alive(s_idx):
                facts.append(("alive", [Number(instance_idx), Number(s_idx)]))
        return list(facts)