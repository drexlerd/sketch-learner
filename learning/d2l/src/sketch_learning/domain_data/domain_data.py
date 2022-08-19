import logging
import dlplan
import tarski

from typing import List
from dataclasses import dataclass

from tarski.io import PDDLReader



@dataclass
class DomainData:
    """ Store data related to a domain. """
    domain_filename: str
    vocabulary_info: dlplan.VocabularyInfo
    syntactic_element_factory: dlplan.SyntacticElementFactory
    feature_generator: dlplan.FeatureGenerator
