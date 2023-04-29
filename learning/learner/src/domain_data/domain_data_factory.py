import logging
import dlplan
import tarski

from tarski.io import PDDLReader

from learner.src.domain_data.domain_data import DomainData


class DomainDataFactory:
    def make_domain_data(self, config):
        logging.info(f"Constructing DomainData for filename {config.domain_filename}")
        domain_filename = config.domain_filename
        # PDDL information
        problem = self._parse_domain_file(domain_filename)
        # Exclude functional predicates =, !=, <, <=, >, >= and predicates with arity 0.
        tarski_predicates = [predicate for predicate in problem.language.predicates if not isinstance(predicate.symbol, tarski.syntax.builtins.BuiltinPredicateSymbol)]
        tarski_constants =  problem.language.constants()
        # Exclude intervals from types.
        tarski_sorts = [sort for sort in problem.language.sorts if not isinstance(sort, tarski.syntax.sorts.Interval)]
        # Store other domain related data here
        vocabulary_info = self._construct_vocabulary_info(tarski_predicates, tarski_constants, tarski_sorts)
        syntactic_element_factory = self._construct_syntactic_element_factory(vocabulary_info)
        feature_generator = self._construct_feature_generator(config)
        return DomainData(domain_filename, vocabulary_info, syntactic_element_factory, feature_generator)

    def _parse_domain_file(self, domain_filename):
        """ Parses the PDDL domain file using Tarski. """
        reader = PDDLReader()
        reader.parse_domain(domain_filename)
        return reader.problem

    def _construct_vocabulary_info(self, tarski_predicates, tarski_constants, tarski_sorts):
        """ Constructs a VocabularyInfo from a domain description. """
        vocabulary_info = dlplan.VocabularyInfo()
        # Add predicates
        for predicate in tarski_predicates:
            vocabulary_info.add_predicate(str(predicate.name), predicate.arity)
            # we allow respective goal versions
            vocabulary_info.add_predicate(str(predicate.name) + "_g", predicate.arity)
            # we allow respective seed versions
            # vocabulary_info.add_predicate(str(predicate.name) + "_r", predicate.arity)
        # Add constants
        for constant in tarski_constants:
            vocabulary_info.add_constant(str(constant.name))
        # Add sorts
        for sort in tarski_sorts:
            vocabulary_info.add_predicate(str(sort.name), 1)
        return vocabulary_info

    def _construct_syntactic_element_factory(self, vocabulary_info):
        """ Constructs an empty factory for constructing elements. """
        return dlplan.SyntacticElementFactory(vocabulary_info)

    def _construct_feature_generator(self, config):
        feature_generator = dlplan.FeatureGenerator()
        feature_generator.set_generate_inclusion_boolean(False)
        feature_generator.set_generate_diff_concept(False)
        feature_generator.set_generate_or_concept(False)
        feature_generator.set_generate_projection_concept(False)
        feature_generator.set_generate_subset_concept(False)
        # feature_generator.set_generate_and_role(False)
        feature_generator.set_generate_compose_role(False)
        feature_generator.set_generate_diff_role(False)
        feature_generator.set_generate_identity_role(False)
        feature_generator.set_generate_not_role(False)
        feature_generator.set_generate_or_role(False)
        feature_generator.set_generate_top_role(False)
        feature_generator.set_generate_transitive_reflexive_closure_role(False)
        return feature_generator
