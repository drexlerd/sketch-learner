from ..fact import Fact


class Condition(Fact):
    """ Defines a feature condition. """
    def __init__(self, name, r_idx, f_idx):
        super().__init__(name)
        self.r_idx = r_idx
        self.f_idx = f_idx

    def __str__(self):
        return f"{self.name}({self.r_idx}, {self.f_idx}).\n"


class C_EQ(Condition):
    def __init__(self, r_idx, f_idx):
        super().__init__("c_eq_fixed", r_idx, f_idx)


class C_GT(Condition):
    def __init__(self, r_idx, f_idx):
        super().__init__("c_gt_fixed", r_idx, f_idx)


class C_POS(Condition):
    def __init__(self, r_idx, f_idx):
        super().__init__("c_pos_fixed", r_idx, f_idx)


class C_NEG(Condition):
    def __init__(self, r_idx, f_idx):
        super().__init__("c_neg_fixed", r_idx, f_idx)
