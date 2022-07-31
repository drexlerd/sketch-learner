from ....instance_data.transition_system import TransitionSystem


class TransitionSystemFactFactory():
    def make_facts(self, instance_idx: int, transition_system: TransitionSystem):
        facts = set()
        for s_idx in range(transition_system.get_num_states()):
            if not transition_system.is_deadend(s_idx):
                facts.add(f"solvable({instance_idx},{s_idx}).")
        return list(facts)