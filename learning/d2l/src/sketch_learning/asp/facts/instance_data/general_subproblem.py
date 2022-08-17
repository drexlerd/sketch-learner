from ....instance_data.subproblem import SubproblemData
from ....iteration_data.state_pair_equivalence_data import StatePairEquivalenceData
from clingo import String, Number


class SubproblemDataFactFactory():
    def make_facts(self, state_pair_equivalence_data: StatePairEquivalenceData, subproblem_data: SubproblemData):
        facts = []
        for root_idx, transitions in subproblem_data.forward_transitions.items():
            facts.append(("expanded", [Number(subproblem_data.id), Number(root_idx)]))
            for transition in transitions:
                r_idx = state_pair_equivalence_data.state_pair_to_r_idx[(transition.source_idx, transition.target_idx)]
                if transition.optimal:
                    facts.append(("optimal_equivalence", [Number(subproblem_data.id), Number(r_idx), Number(transition.source_idx), Number(transition.target_idx)]))
                else:
                    facts.append(("suboptimal_equivalence", [Number(subproblem_data.id), Number(r_idx), Number(transition.source_idx), Number(transition.target_idx)]))
        subproblem_data.print()
        return list(facts)