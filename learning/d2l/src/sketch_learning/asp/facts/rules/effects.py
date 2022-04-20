from ..fact import Fact


class Effect(Fact):
    """ Defines a feature effect. """
    def __init__(self, name, r_idx, f_idx):
        super().__init__(name)
        self.r_idx = r_idx
        self.f_idx = f_idx

    def __str__(self):
        return f"{self.name}({self.r_idx}, {self.f_idx}).\n"


class E_INC(Effect):
    def __init__(self, r_idx, f_idx):
        super().__init__("e_inc_fixed", r_idx, f_idx)


class E_DEC(Effect):
    def __init__(self, r_idx, f_idx):
        super().__init__("e_dec_fixed", r_idx, f_idx)


class E_POS(Effect):
    def __init__(self, r_idx, f_idx):
        super().__init__("e_pos_fixed", r_idx, f_idx)


class E_NEG(Effect):
    def __init__(self, r_idx, f_idx):
        super().__init__("e_neg_fixed", r_idx, f_idx)


class E_BOT(Effect):
    def __init__(self, r_idx, f_idx):
        super().__init__("e_bot_fixed", r_idx, f_idx)
