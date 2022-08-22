from ....instance_data.transition_system import TransitionSystem
from ....iteration_data.instance_feature_data import InstanceFeatureData
from clingo import String, Number

class TransitionSystemFactFactory():
    def make_facts(self, instance_idx: int, transition_system: TransitionSystem, instance_feature_data: InstanceFeatureData):
        facts = []
        for s_idx in transition_system.s_idx_to_dlplan_state.keys():
            if not transition_system.is_deadend(s_idx):
                facts.append(("solvable", [Number(instance_idx), Number(s_idx)]))
            if transition_system.is_goal(s_idx):
                facts.append(("goal", [Number(instance_idx), Number(s_idx)]))
            else:
                facts.append(("nongoal", [Number(instance_idx), Number(s_idx)]))
            for f_idx, f_val in enumerate(instance_feature_data.boolean_feature_valuations[s_idx]):
                facts.append(("value", [Number(instance_idx), Number(s_idx), Number(f_idx), Number(f_val)]))
            for f_idx, f_val in enumerate(instance_feature_data.numerical_feature_valuations[s_idx]):
                facts.append(("value", [Number(instance_idx), Number(s_idx), Number(f_idx + len(instance_feature_data.boolean_feature_valuations[s_idx])), Number(f_val)]))
        return list(facts)