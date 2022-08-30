from clingo import Number

from ....instance_data.state_pair_classifier import StatePairClassifier, StatePairClassification
from ....iteration_data.state_pair_equivalence import StatePairEquivalence


class StatePairClassifierFactFactory:
    def make_facts(self, instance_idx: int, state_pair_classifier: StatePairClassifier, state_pair_equivalence: StatePairEquivalence):
        facts = []
        for s_idx in state_pair_classifier.expanded_s_idxs:
            facts.append(("expanded", [Number(instance_idx), Number(s_idx)]))
        for state_pair, classification in state_pair_classifier.state_pair_to_classification.items():
            r_idx = state_pair_equivalence.state_pair_to_r_idx[(state_pair.source_idx, state_pair.target_idx)]
            if classification == StatePairClassification.DELTA_OPTIMAL:
                facts.append(("delta_optimal", [Number(instance_idx), Number(r_idx), Number(state_pair.source_idx), Number(state_pair.target_idx)]))
            elif classification == StatePairClassification.NOT_DELTA_OPTIMAL:
                facts.append(("not_delta_optimal", [Number(instance_idx), Number(r_idx), Number(state_pair.source_idx), Number(state_pair.target_idx)]))
            else:
                raise Exception("StatePairClassifierFactFactory::make_facts - unknown StatePairClassification")
        return facts