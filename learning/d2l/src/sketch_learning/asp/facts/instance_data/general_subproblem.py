from ....instance_data.general_subproblem import GeneralSubproblemData
from ....iteration_data.state_pair_equivalence_data import StatePairEquivalenceData
from clingo import String, Number


class GeneralSubproblemDataFactFactory():
    def make_facts(self, instance_idx: int, state_pair_equivalence_data: StatePairEquivalenceData, general_subproblem_data: GeneralSubproblemData):
        facts = []
        for root_idx, transitionss in general_subproblem_data.forward_transitions.items():
            for g_idx, transitions in enumerate(transitionss):
                facts.append(("expanded", [Number(instance_idx), Number(g_idx), Number(root_idx)]))
                for transition in transitions:
                    r_idx = state_pair_equivalence_data.state_pair_to_r_idx[(transition.source_idx, transition.target_idx)]
                    if transition.optimal:
                        facts.append(("optimal_equivalence", [Number(instance_idx), Number(g_idx), Number(r_idx), Number(transition.source_idx), Number(transition.target_idx)]))
                    else:
                        facts.append(("suboptimal_equivalence", [Number(instance_idx), Number(g_idx), Number(r_idx), Number(transition.source_idx), Number(transition.target_idx)]))
        return list(facts)