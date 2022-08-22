from re import sub
from ....instance_data.subproblem import Subproblem
from ....iteration_data.instance_feature_data import InstanceFeatureData
from ....iteration_data.state_pair_equivalence import StatePairEquivalence
from clingo import String, Number


class SubproblemFactFactory():
    def make_facts(self, state_pair_equivalence_data: StatePairEquivalence, subproblem_data: Subproblem, instance_feature_data: InstanceFeatureData):
        facts = []
        for root_idx, transitions in subproblem_data.forward_transitions.items():
            facts.append(("expanded", [Number(subproblem_data.id), Number(root_idx)]))
            for transition in transitions:
                r_idx = state_pair_equivalence_data.state_pair_to_r_idx[(transition.source_idx, transition.target_idx)]
                if transition.optimal:
                    facts.append(("optimal_equivalence", [Number(subproblem_data.id), Number(r_idx), Number(transition.source_idx), Number(transition.target_idx)]))
                else:
                    facts.append(("suboptimal_equivalence", [Number(subproblem_data.id), Number(r_idx), Number(transition.source_idx), Number(transition.target_idx)]))
        for s_idx in subproblem_data.expanded_states:
            facts.append(("nongoal", [Number(subproblem_data.id), Number(s_idx)]))
        for s_idx in subproblem_data.goal_states:
            facts.append(("goal", [Number(subproblem_data.id), Number(s_idx)]))
        for s_idx in subproblem_data.generated_states:
            for f_idx, f_val in enumerate(instance_feature_data.boolean_feature_valuations[s_idx]):
                facts.append(("value", [Number(subproblem_data.id), Number(s_idx), Number(f_idx), Number(f_val)]))
            for f_idx, f_val in enumerate(instance_feature_data.numerical_feature_valuations[s_idx]):
                facts.append(("value", [Number(subproblem_data.id), Number(s_idx), Number(f_idx + len(instance_feature_data.boolean_feature_valuations[s_idx])), Number(f_val)]))
        return list(facts)