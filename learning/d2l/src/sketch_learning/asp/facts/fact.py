import abc


class Fact(abc.ABC):
    def __init__(self, name):
        self.name = name
