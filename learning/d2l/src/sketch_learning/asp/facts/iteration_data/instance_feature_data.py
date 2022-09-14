from clingo import Number

from ....instance_data.instance_data import InstanceData


class InstanceFeatureDataFactFactory:
    def make_facts(self, instance_data: InstanceData):
        facts = []
        for s_idx in instance_data.state_pair_classifier.generated_s_idxs:
            for f_idx, f_val in enumerate(instance_data.instance_feature_data.boolean_feature_valuations[s_idx]):
                facts.append(("value", [Number(instance_data.id), Number(s_idx), Number(f_idx), Number(f_val)]))
            for f_idx, f_val in enumerate(instance_data.instance_feature_data.numerical_feature_valuations[s_idx]):
                facts.append(("value", [Number(instance_data.id), Number(s_idx), Number(f_idx + len(instance_data.instance_feature_data.boolean_feature_valuations[s_idx])), Number(f_val)]))
        return facts
