import logging

from dlplan.core import VocabularyInfo, SyntacticElementFactory
from dlplan.policy import PolicyFactory

from ..domain_data.domain_data import DomainData


def compute_domain_data(domain_filename: str, vocabulary_info: VocabularyInfo) -> DomainData:
    logging.info("Constructing DomainData for filename %s", domain_filename)
    syntactic_element_factory = SyntacticElementFactory(vocabulary_info)
    policy_builder = PolicyFactory(syntactic_element_factory)
    return DomainData(domain_filename, vocabulary_info, policy_builder, syntactic_element_factory)