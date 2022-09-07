from re import sub
import dlplan
import logging

from typing import  List
from termcolor import colored

from .instance_data.return_codes import ReturnCode

from .returncodes import ExitCode
from .asp.returncodes import ClingoExitCode
from .util.command import read_file
from .domain_data.domain_data_factory import DomainDataFactory
from .instance_data.instance_data import InstanceData
from .instance_data.instance_data_factory import InstanceDataFactory
from .instance_data.state_pair_classifier import StatePairClassifier
from .instance_data.state_pair_classifier_factory import StatePairClassifierFactory
from .instance_data.tuple_graph_factory import TupleGraphFactory
from .instance_data.tuple_graph import TupleGraph
from .iteration_data.domain_feature_data_factory import DomainFeatureDataFactory
from .iteration_data.instance_feature_data_factory import InstanceFeatureDataFactory
from .iteration_data.state_pair_equivalence_factory import StatePairEquivalenceFactory
from .iteration_data.dlplan_policy_factory import DlplanPolicyFactory
from .iteration_data.sketch import Sketch
from .asp.policy_asp_factory import PolicyASPFactory
from .util.timer import CountDownTimer
from .learning_sketches_step import learn_sketch


def run(config, data, rng):
    logging.info(colored(f"Initializing DomainData...", "blue", "on_grey"))
    domain_data = DomainDataFactory().make_domain_data(config)
    logging.info(colored(f"..done", "blue", "on_grey"))

    logging.info(colored(f"Initializing InstanceDatas...", "blue", "on_grey"))
    instance_datas = InstanceDataFactory().make_instance_datas(config, domain_data)
    logging.info(colored(f"..done", "blue", "on_grey"))

    logging.info(colored(f"Initializing Sketch...", "blue", "on_grey"))
    sketch = Sketch(dlplan.PolicyReader().read("\n".join(read_file(config.sketch_filename)), domain_data.syntactic_element_factory), config.width)
    logging.info(colored(f"..done", "blue", "on_grey"))

    solution_policies = []
    structurally_minimized_solution_policies = []
    empirically_minimized_solution_policies = []
    for rule in sketch.get_rules():
        print("Sketch:")
        print(sketch.dlplan_policy.compute_repr())
        print("Sketch rule:", rule.dlplan_rule.compute_repr())

        logging.info(colored(f"Initializing Subproblems...", "blue", "on_grey"))
        subproblem_instance_datas = []
        state_pair_classifiers_by_instance = []
        tuple_graphs_by_instance = []
        for instance_data in instance_datas:
            for s_idx in instance_data.transition_system.s_idx_to_dlplan_state.keys():
                if not instance_data.transition_system.is_solvable():
                    # we do not want to solve subproblems that are deadends in the original problem
                    continue
                subproblem_instance_data = InstanceDataFactory().make_subproblem_instance_data(len(subproblem_instance_datas), instance_data, s_idx, rule)
                if not subproblem_instance_data.transition_system.is_solvable():
                    continue

                # Create tuple graph for subproblem instance
                tuple_graphs = TupleGraphFactory(width=0).make_tuple_graphs(subproblem_instance_data)

                # Classify state pairs and restrict the transition system according to relevant parts.
                state_pair_classifier = StatePairClassifierFactory(config.delta).make_state_pair_classifier(config, subproblem_instance_data, tuple_graphs)

                # Restrict transition system to subset of states
                subproblem_instance_data.transition_system.restrict_to_subset_of_states(
                    state_pair_classifier.expanded_s_idxs,
                    state_pair_classifier.generated_s_idxs)
                if not subproblem_instance_data.transition_system.is_solvable() or \
                    subproblem_instance_data.transition_system.is_trivially_solvable():
                    continue
                # Re-create tuple graphs are restricting transition system
                tuple_graphs = TupleGraphFactory(width=0).make_tuple_graphs(subproblem_instance_data)

                subproblem_instance_datas.append(subproblem_instance_data)
                tuple_graphs_by_instance.append(tuple_graphs)
                state_pair_classifiers_by_instance.append(state_pair_classifier)
        print("Number of subproblems:", len(subproblem_instance_datas))
        logging.info(colored(f"..done", "blue", "on_grey"))

        sketch, structurally_minimized_sketch, empirically_minimized_sketch = learn_sketch(config, domain_data, subproblem_instance_datas, tuple_graphs_by_instance, state_pair_classifiers_by_instance, make_policy_asp_factory)
        solution_policies.append(sketch)
        structurally_minimized_solution_policies.append(structurally_minimized_sketch)
        empirically_minimized_solution_policies.append(empirically_minimized_sketch)

    logging.info(colored("Summary:", "yellow", "on_grey"))
    print("Input sketch:")
    print(sketch.dlplan_policy.compute_repr())
    print("Learned policies by rule:")
    for rule in sketch.get_rules():
        print("Rule", rule.id, rule.dlplan_rule.compute_repr())
        if solution_policies[rule.id] is not None:
            print("Resulting policy:")
            print(solution_policies[rule.id].print())
        else:
            print("No policy found.")
    print()
    print("Learned structurally minimized policies by rule:")
    for rule in sketch.get_rules():
        print("Rule", rule.id, rule.dlplan_rule.compute_repr())
        if structurally_minimized_solution_policies[rule.id] is not None:
            print("Resulting structurally minimized sketch:")
            print(structurally_minimized_solution_policies[rule.id].print())
        else:
            print("No policy found.")
    print()
    print("Learned empirically minimized policies by rule:")
    for rule in sketch.get_rules():
        print("Rule", rule.id, rule.dlplan_rule.compute_repr())
        if empirically_minimized_solution_policies[rule.id] is not None:
            print("Resulting empirically minimized sketch:")
            print(empirically_minimized_solution_policies[rule.id].print())
        else:
            print("No policy found.")
    return ExitCode.Success, None


def make_policy_asp_factory(config):
    return PolicyASPFactory(config)




