from dataclasses import dataclass


@dataclass
class LearningStatistics:
    num_training_instances: int = 0
    num_selected_training_instances: int = 0
    num_states_in_selected_training_instances: int = 0
    num_states_in_complete_selected_training_instances: int = 0
    num_features_in_pool: int = 0

    def print(self):
        print("LearningStatistics:")
        print("    num_training_instances:", self.num_training_instances)
        print("    num_selected_training_instances (|P|):", self.num_selected_training_instances)
        print("    num_states_in_selected_training_instances (|S|):", self.num_states_in_selected_training_instances)
        print("    num_states_in_complete_selected_training_instances (|S|):", self.num_states_in_complete_selected_training_instances)
        print("    num_features_in_pool (|F|):", self.num_features_in_pool)
