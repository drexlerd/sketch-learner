from ....instance_data.transition_system import TransitionSystem
from clingo import String, Number

class TransitionSystemFactFactory():
    def make_facts(self, instance_idx: int, transition_system: TransitionSystem):
        facts = []
        for s_idx in range(transition_system.get_num_states()):
            if not transition_system.is_deadend(s_idx):
                facts.append(("solvable", [Number(instance_idx), Number(s_idx)]))
            #if transition_system.is_goal(s_idx):
            #    facts.append(("goal"), [Number(instance_idx), Number(s_idx)])
            #else:
            #    facts.append(("nongoal"), [Number(instance_idx), Number(s_idx)])
        return list(facts)