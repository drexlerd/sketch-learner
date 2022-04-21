from ..fact import Fact


class TerminationLoop(Fact):
    """ Defines a loop in the termination graph. """
    def __init__(self, r_idx):
        super().__init__("termination_loop")
        self.r_idx = r_idx

    def __str__(self):
        return f"{self.name}({self.r_idx}).\n"
