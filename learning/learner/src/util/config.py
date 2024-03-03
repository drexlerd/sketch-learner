from enum import Enum


class EncodingType(Enum):
    """
    D2 is the encoding related to Francès et al. (AAAI2021): https://arxiv.org/abs/2101.00692
    EXPLICIT is the encoding from Drexler et al. (ICAPS2022): https://arxiv.org/abs/2203.14852
    """
    D2 = 0
    EXPLICIT = 1
