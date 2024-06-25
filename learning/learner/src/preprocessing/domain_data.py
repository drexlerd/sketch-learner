from dataclasses import dataclass

import dlplan.core as dlplan_core
import dlplan.policy as dlplan_policy

@dataclass
class DomainData:
    """ Immutable data class. """
    _domain_filename: str
    _vocabulary_info: dlplan_core.VocabularyInfo
    _policy_builder: dlplan_policy.PolicyFactory
    _syntactic_element_factory: dlplan_core.SyntacticElementFactory

    @property
    def domain_filename(self):
        return self._domain_filename

    @property
    def vocabulary_info(self):
        return self._vocabulary_info

    @property
    def policy_builder(self):
        return self._policy_builder

    @property
    def syntactic_element_factory(self):
        return self._syntactic_element_factory
