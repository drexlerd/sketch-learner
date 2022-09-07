import logging

from termcolor import colored
from typing import List
from sketch_learning.asp.policy_asp_factory import PolicyASPFactory

from sketch_learning.asp.returncodes import ClingoExitCode

from .asp.sketch_asp_factory import SketchASPFactory
from .domain_data.domain_data_factory import DomainDataFactory
from .instance_data.instance_data import InstanceData
from .instance_data.instance_data_factory import InstanceDataFactory
from .instance_data.tuple_graph import TupleGraph
from .instance_data.tuple_graph_factory import TupleGraphFactory
from .iteration_data.domain_feature_data_factory import DomainFeatureDataFactory
from .iteration_data.instance_feature_data_factory import InstanceFeatureDataFactory
from .iteration_data.dlplan_policy_factory import DlplanPolicyFactory
from .iteration_data.sketch import Sketch
from .iteration_data.state_pair_equivalence_factory import StatePairEquivalenceFactory
from .iteration_data.tuple_graph_equivalence_data_factory import  TupleGraphEquivalenceFactory
from .instance_data.state_pair_classifier_factory import StatePairClassifierFactory
from .instance_data.state_pair_classifier import StatePairClassifier
from .returncodes import ExitCode
from .util.timer import CountDownTimer


def run(config, data, rng):
    logging.info(colored(f"Initializing DomainData...", "blue", "on_grey"))
    domain_data = DomainDataFactory().make_domain_data(config)
    logging.info(colored(f"..done", "blue", "on_grey"))

    logging.info(colored(f"Initializing InstanceDatas...", "blue", "on_grey"))
    instance_datas = InstanceDataFactory().make_instance_datas(config, domain_data)
    logging.info(colored(f"..done", "blue", "on_grey"))

    logging.info(colored(f"Initializing TupleGraphs...", "blue", "on_grey"))
    tuple_graphs_by_instance = [TupleGraphFactory(config.width).make_tuple_graphs(instance_data) for instance_data in instance_datas]
    logging.info(colored(f"..done", "blue", "on_grey"))

    logging.info(colored(f"Initializing StatePairClassifiers...", "blue", "on_grey"))
    state_pair_classifiers_by_instance = [StatePairClassifierFactory(config.delta).make_state_pair_classifier(config, instance_data, tuple_graphs) for instance_data, tuple_graphs in zip(instance_datas, tuple_graphs_by_instance)]
    logging.info(colored(f"..done", "blue", "on_grey"))

    sketch = learn_sketch(config, domain_data, instance_datas, tuple_graphs_by_instance, state_pair_classifiers_by_instance, make_sketch_asp_factory)

    return ExitCode.Success, None


def compute_smallest_unsolved_instance(sketch: Sketch, instance_datas: List[InstanceData], tuple_graphs_by_instance: List[List[TupleGraph]], state_pair_classifiers_by_instance: List[StatePairClassifier]):
    for instance_data, tuple_graphs, state_pair_classifier in zip(instance_datas, tuple_graphs_by_instance, state_pair_classifiers_by_instance):
        if not sketch.solves(instance_data, tuple_graphs, state_pair_classifier):
            return instance_data
    return None


def make_sketch_asp_factory(config):
    return SketchASPFactory(config)


def learn_sketch(config, domain_data, instance_datas, tuple_graphs_by_instance, state_pair_classifiers_by_instance, make_asp_factory):
    i = 0
    selected_instance_idxs = [0]
    timer = CountDownTimer(config.timeout)
    while not timer.is_expired():
        logging.info(colored(f"Iteration: {i}", "red", "on_grey"))
        selected_instance_datas = [instance_datas[subproblem_idx] for subproblem_idx in selected_instance_idxs]
        tuple_graphs_by_selected_instance = [tuple_graphs_by_instance[subproblem_idx] for subproblem_idx in selected_instance_idxs]
        state_pair_classifiers_by_selected_instance = [state_pair_classifiers_by_instance[subproblem_idx] for subproblem_idx in selected_instance_idxs]
        print(f"Number of selected instances: {len(selected_instance_datas)}")
        print(f"Indices of selected instances:", selected_instance_idxs)

        logging.info(colored(f"Initializing DomainFeatureData...", "blue", "on_grey"))
        domain_feature_data_factory = DomainFeatureDataFactory()
        domain_feature_data = domain_feature_data_factory.make_domain_feature_data_from_subproblems(config, domain_data, selected_instance_datas, state_pair_classifiers_by_selected_instance)
        domain_feature_data_factory.statistics.print()
        logging.info(colored(f"..done", "blue", "on_grey"))

        logging.info(colored(f"Initializing InstanceFeatureDatas...", "blue", "on_grey"))
        instance_feature_datas_by_selected_instance = [InstanceFeatureDataFactory().make_instance_feature_data(instance_data, domain_feature_data) for instance_data in selected_instance_datas]
        logging.info(colored(f"..done", "blue", "on_grey"))

        logging.info(colored(f"Initializing StatePairEquivalenceDatas...", "blue", "on_grey"))
        state_pair_equivalence_factory = StatePairEquivalenceFactory()
        rule_equivalences, state_pair_equivalences_by_selected_instance = state_pair_equivalence_factory.make_state_pair_equivalences(domain_feature_data, state_pair_classifiers_by_selected_instance, instance_feature_datas_by_selected_instance)
        logging.info(colored(f"..done", "blue", "on_grey"))

        logging.info(colored(f"Initializing TupleGraphEquivalences...", "blue", "on_grey"))
        tuple_graph_equivalences_by_selected_instance = [TupleGraphEquivalenceFactory().make_tuple_graph_equivalence_datas(instance_data, tuple_graphs, state_pair_equivalences) for instance_data, tuple_graphs, state_pair_equivalences in zip(selected_instance_datas, tuple_graphs_by_selected_instance, state_pair_equivalences_by_selected_instance)]
        logging.info(colored(f"..done", "blue", "on_grey"))

        asp_factory = make_asp_factory(config)
        facts = asp_factory.make_facts(domain_feature_data, rule_equivalences, selected_instance_datas, tuple_graphs_by_selected_instance, tuple_graph_equivalences_by_selected_instance, state_pair_equivalences_by_selected_instance, state_pair_classifiers_by_selected_instance, instance_feature_datas_by_selected_instance)
        d2_facts = asp_factory.make_initial_d2_facts(state_pair_classifiers_by_selected_instance, state_pair_equivalences_by_selected_instance)
        print("Number of initial D2 facts:", len(d2_facts))
        print("Number of D2 facts:", len(d2_facts), "of", len(rule_equivalences.rules) ** 2)
        facts.extend(list(d2_facts))

        logging.info(colored(f"Grounding Logic Program...", "blue", "on_grey"))
        asp_factory.ground(facts)
        logging.info(colored(f"..done", "blue", "on_grey"))

        logging.info(colored(f"Solving Logic Program...", "blue", "on_grey"))
        symbols, returncode = asp_factory.solve()
        logging.info(colored(f"..done", "blue", "on_grey"))
        asp_factory.print_statistics()
        if returncode in [ClingoExitCode.UNSATISFIABLE]:
            print(colored("ASP is UNSAT", "red", "on_grey"))
            print(colored("No sketch exists that solves all geneneral subproblems!", "red", "on_grey"))
            return None
        sketch = Sketch(DlplanPolicyFactory().make_dlplan_policy_from_answer_set_d2(symbols, domain_feature_data, rule_equivalences), width=0)
        print("Learned sketch:")
        print(sketch.dlplan_policy.compute_repr())

        # Iteratively add D2-separation constraints
        while True:
            if compute_smallest_unsolved_instance(sketch, instance_datas, tuple_graphs_by_instance, state_pair_classifiers_by_instance) is None:
                # Stop adding D2-separation constraints
                # if sketch solves all training instances by luck
                break

            asp_factory = make_asp_factory(config)
            facts = asp_factory.make_facts(domain_feature_data, rule_equivalences, selected_instance_datas, tuple_graphs_by_selected_instance, tuple_graph_equivalences_by_selected_instance, state_pair_equivalences_by_selected_instance, state_pair_classifiers_by_selected_instance, instance_feature_datas_by_selected_instance)
            unsatisfied_d2_facts = asp_factory.make_unsatisfied_d2_facts(symbols, rule_equivalences)
            d2_facts.update(unsatisfied_d2_facts)
            facts.extend(list(d2_facts))
            print("Number of unsatisfied D2 facts:", len(unsatisfied_d2_facts))
            print("Number of D2 facts:", len(d2_facts), "of", len(rule_equivalences.rules) ** 2)
            if not unsatisfied_d2_facts:
                break

            logging.info(colored(f"Grounding Logic Program...", "blue", "on_grey"))
            asp_factory.ground(facts)
            logging.info(colored(f"..done", "blue", "on_grey"))

            logging.info(colored(f"Solving Logic Program...", "blue", "on_grey"))
            symbols, returncode = asp_factory.solve()
            logging.info(colored(f"..done", "blue", "on_grey"))

            if returncode in [ClingoExitCode.UNSATISFIABLE]:
                print(colored("ASP is UNSAT", "red", "on_grey"))
                print(colored("No sketch exists that solves all geneneral subproblems!", "red", "on_grey"))
                return None
            asp_factory.print_statistics()
            sketch = Sketch(DlplanPolicyFactory().make_dlplan_policy_from_answer_set_d2(symbols, domain_feature_data, rule_equivalences), width=0)
            logging.info("Learned the following sketch:")
            print(sketch.dlplan_policy.str())

        logging.info(colored(f"Verifying learned sketch...", "blue", "on_grey"))
        assert compute_smallest_unsolved_instance(sketch, selected_instance_datas, tuple_graphs_by_selected_instance, state_pair_classifiers_by_selected_instance) is None
        smallest_unsolved_instance = compute_smallest_unsolved_instance(sketch, instance_datas, tuple_graphs_by_instance, state_pair_classifiers_by_instance)
        logging.info(colored(f"..done", "blue", "on_grey"))

        logging.info(colored("Iteration summary:", "yellow", "on_grey"))
        domain_feature_data_factory.statistics.print()
        state_pair_equivalence_factory.statistics.print()

        if smallest_unsolved_instance is None:
            print(colored("Sketch solves all instances!", "red", "on_grey"))
            break
        else:
            if smallest_unsolved_instance.id > max(selected_instance_idxs):
                selected_instance_idxs = [smallest_unsolved_instance.id]
            else:
                selected_instance_idxs.append(smallest_unsolved_instance.id)
        i += 1

    logging.info(colored("Summary:", "green", "on_grey"))
    print("Number of training instances:", len(instance_datas))
    print("Number of training instances included in the ASP:", len(selected_instance_datas))
    print("Number of states included in the ASP:", sum([instance_data.transition_system.get_num_states() for instance_data in selected_instance_datas]))
    print("Number of features in the pool:", len(domain_feature_data.boolean_features) + len(domain_feature_data.numerical_features))
    print("Numer of sketch rules:", len(sketch.dlplan_policy.get_rules()))
    print("Number of selected features:", len(sketch.dlplan_policy.get_boolean_features()) + len(sketch.dlplan_policy.get_numerical_features()))
    print("Maximum complexity of selected feature:", max([0] + [boolean_feature.get_boolean().compute_complexity() for boolean_feature in sketch.dlplan_policy.get_boolean_features()] + [numerical_feature.get_numerical().compute_complexity() for numerical_feature in sketch.dlplan_policy.get_numerical_features()]))
    print("Resulting sketch:")
    print(sketch.dlplan_policy.str())
    return sketch