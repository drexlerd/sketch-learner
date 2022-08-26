from clingo import Number

from ....iteration_data.instance_feature_data import InstanceFeatureData
from ....instance_data.state_pair_classifier import StatePairClassifier


class InstanceFeatureDataFactFactory:
    def make_facts(self, instance_idx: int, instance_feature_data: InstanceFeatureData, state_pair_classifier: StatePairClassifier):
        facts = []
        for s_idx in state_pair_classifier.generated_s_idxs:
            for f_idx, f_val in enumerate(instance_feature_data.boolean_feature_valuations[s_idx]):
                facts.append(("value", [Number(instance_idx), Number(s_idx), Number(f_idx), Number(f_val)]))
            for f_idx, f_val in enumerate(instance_feature_data.numerical_feature_valuations[s_idx]):
                facts.append(("value", [Number(instance_idx), Number(s_idx), Number(f_idx + len(instance_feature_data.boolean_feature_valuations[s_idx])), Number(f_val)]))
        return facts
