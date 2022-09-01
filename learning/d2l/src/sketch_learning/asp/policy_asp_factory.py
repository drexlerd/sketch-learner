from .asp_factory import ASPFactory


class PolicyASPFactory(ASPFactory):
    def __init__(self, config):
        super().__init__(config)
        self.ctl.load(str(config.asp_policy_location))
