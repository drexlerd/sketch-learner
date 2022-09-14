from clingo import Number

from ....instance_data.instance_data import InstanceData
from ....instance_data.state_pair_classifier import StatePairClassification


class StatePairClassifierFactFactory:
    def make_facts(self, instance_data: InstanceData):
        facts = []
        for state_pair, classification in instance_data.state_pair_classifier.state_pair_to_classification.items():
            r_idx = instance_data.state_pair_equivalence.state_pair_to_r_idx[state_pair]
            if classification == StatePairClassification.DELTA_OPTIMAL:
                facts.append(("delta_optimal", [Number(instance_data.id), Number(r_idx), Number(state_pair.source_idx), Number(state_pair.target_idx)]))
            elif classification == StatePairClassification.NOT_DELTA_OPTIMAL:
                facts.append(("not_delta_optimal", [Number(instance_data.id), Number(r_idx), Number(state_pair.source_idx), Number(state_pair.target_idx)]))
            else:
                raise Exception("StatePairClassifierFactFactory::make_facts - unknown StatePairClassification")
        return facts