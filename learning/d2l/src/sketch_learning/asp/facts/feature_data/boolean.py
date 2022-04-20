from ..fact import Fact


class Boolean(Fact):
    """ Defines a boolean feature. """
    def __init__(self, f_idx):
        super().__init__("boolean")
        self.f_idx = f_idx

    def __str__(self):
        return f"{self.name}({self.f_idx}).\n"
