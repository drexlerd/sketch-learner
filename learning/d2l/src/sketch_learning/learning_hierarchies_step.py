import dlplan
import logging
from .returncodes import ExitCode
from .preprocessing import preprocess_instances
from .util.command import execute, write_file, read_file, create_experiment_workspace
from .instance_data.general_subproblem import GeneralSubproblemDataFactory
from .iteration_data.state_pair_data import StatePairDataFactory
from .iteration_data.feature_data import DomainFeatureDataFactory, InstanceFeatureDataFactory
from .iteration_data.equivalence_data import StatePairEquivalenceDataFactory
from .iteration_data.sketch_factory import SketchFactory
from .asp.policy_asp_factory import PolicyASPFactory
from .util.timer import Timer, CountDownTimer

def run(config, data, rng):
    domain_data, instance_datas = preprocess_instances(config)
    sketch = dlplan.PolicyReader().read("\n".join(read_file(config.sketch_filename)), domain_data.syntactic_element_factory)
    print(sketch.compute_repr())

    i = 0
    instance_data = instance_datas[0]
    selected_instance_datas = []
    largest_unsolved_instance_idx = 0
    timer = CountDownTimer(config.timeout)
    while not timer.is_expired():
        logging.info(f"Iteration: {i}")
        selected_instance_datas.append(instance_data)
        for rule in sketch.get_rules():
            print(rule.compute_repr())
            general_subproblem_datas = GeneralSubproblemDataFactory().make_general_subproblems(selected_instance_datas, sketch, rule)
            state_pair_datas = StatePairDataFactory().make_state_pairs_from_general_subproblems(general_subproblem_datas)
            dlplan_states = []
            for selected_instance_data, state_pair_data in zip(selected_instance_datas, state_pair_datas):
                dlplan_states.extend([selected_instance_data.transition_system.states_by_index[s_idx] for s_idx in state_pair_data.states])
            domain_feature_data = DomainFeatureDataFactory().make_domain_feature_data(config, domain_data, dlplan_states)
            instance_feature_datas = InstanceFeatureDataFactory().make_instance_feature_datas(selected_instance_datas, domain_feature_data)
            rule_equivalence_data, state_pair_equivalence_datas = StatePairEquivalenceDataFactory().make_equivalence_data(state_pair_datas, domain_feature_data, instance_feature_datas)

            policy_asp_factory = PolicyASPFactory(config)
            facts = PolicyASPFactory(config).make_facts(selected_instance_datas, domain_feature_data, rule_equivalence_data, state_pair_equivalence_datas, general_subproblem_datas)
            policy_asp_factory.ground(facts)
            model = policy_asp_factory.solve()
            policy_asp_factory.print_statistics()
            policy = SketchFactory().make_sketch(model, domain_feature_data, config.width)
            print("Learned policy:")
            print(policy.policy.compute_repr())
        break
    return ExitCode.Success, None