import dlplan
import logging
from .returncodes import ExitCode
from .preprocessing import preprocess_instances
from .util.command import execute, write_file, read_file, create_experiment_workspace
from .instance_data.general_subproblem import GeneralSubproblemDataFactory
from .iteration_data.state_pair_data import StatePairDataFactory
from .iteration_data.feature_data import DomainFeatureDataFactory, InstanceFeatureDataFactory
from .iteration_data.state_pair_equivalence_data import StatePairEquivalenceDataFactory
from .iteration_data.dlplan_policy_factory import DlplanPolicyFactory
from .iteration_data.policy import Policy
from .asp.policy_asp_factory import PolicyASPFactory
from .util.timer import Timer, CountDownTimer

def run(config, data, rng):
    domain_data, instance_datas = preprocess_instances(config)
    sketch = dlplan.PolicyReader().read("\n".join(read_file(config.sketch_filename)), domain_data.syntactic_element_factory)
    print(sketch.compute_repr())
    general_subproblem_datas_by_rule = []
    for rule in sketch.get_rules():
        print(rule.compute_repr())
        general_subproblem_data = GeneralSubproblemDataFactory().make_general_subproblems(instance_datas, sketch, rule)
        general_subproblem_datas_by_rule.append(general_subproblem_data)

    for r_idx, rule in enumerate(sketch.get_rules()):
        i = 0
        selected_instance_idxs = [0]
        timer = CountDownTimer(config.timeout)
        while not timer.is_expired():
            logging.info(f"Iteration: {i}")
            selected_instance_datas = [instance_datas[instance_idx] for instance_idx in selected_instance_idxs]
            selected_general_subproblem_datas = [general_subproblem_datas_by_rule[r_idx][instance_idx] for instance_idx in selected_instance_idxs]
            state_pair_datas = StatePairDataFactory().make_state_pairs_from_general_subproblems(selected_general_subproblem_datas)
            dlplan_states = []
            for selected_instance_data, state_pair_data in zip(selected_instance_datas, state_pair_datas):
                dlplan_states.extend([selected_instance_data.transition_system.states_by_index[s_idx] for s_idx in state_pair_data.states])
            domain_feature_data = DomainFeatureDataFactory().make_domain_feature_data(config, domain_data, dlplan_states)
            instance_feature_datas = InstanceFeatureDataFactory().make_instance_feature_datas(selected_instance_datas, domain_feature_data)
            rule_equivalence_data, state_pair_equivalence_datas = StatePairEquivalenceDataFactory().make_equivalence_data(state_pair_datas, domain_feature_data, instance_feature_datas)

            policy_asp_factory = PolicyASPFactory(config)
            facts = PolicyASPFactory(config).make_facts(selected_instance_datas, domain_feature_data, rule_equivalence_data, state_pair_equivalence_datas, selected_general_subproblem_datas)
            policy_asp_factory.ground(facts)
            model = policy_asp_factory.solve()
            policy_asp_factory.print_statistics()
            policy = Policy(DlplanPolicyFactory().make_dlplan_policy_from_answer_set(model, domain_feature_data))
            print("Learned policy:")
            print(policy.policy.compute_repr())
            for selected_instance_data, general_subproblem_data in zip(selected_instance_datas, selected_general_subproblem_datas):
                assert policy.solves(selected_instance_data, general_subproblem_data)

            all_solved = True
            for instance_idx, (instance_data, general_subproblem) in enumerate(zip(instance_datas, general_subproblem_datas_by_rule[r_idx])):
                if not policy.solves(instance_data, general_subproblem):
                    print("Policy fails to solve: ", instance_idx)
                    selected_instance_idxs.append(instance_idx)
                    all_solved = False
                    break
            if all_solved:
                print("Policy solves all general subproblems!")
                break
            i += 1
    return ExitCode.Success, None