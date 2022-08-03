from operator import eq
import sys
import os
import shutil
import logging
import dlplan

from collections import defaultdict
from pathlib import Path

from .returncodes import ExitCode
from .util.command import execute, write_file, read_file, create_experiment_workspace
from .util.timer import Timer, CountDownTimer

from .instance_data.instance_data import InstanceData
from .domain_data.domain_data import DomainData
from .iteration_data.iteration_data import IterationData
from .iteration_data.feature_data import DomainFeatureDataFactory, InstanceFeatureDataFactory
from .iteration_data.dlplan_policy_factory import DlplanPolicyFactory
from .iteration_data.sketch import Sketch
from .iteration_data.state_pair_equivalence_data import StatePairEquivalenceDataFactory
from .iteration_data.tuple_graph_equivalence_data import  TupleGraphEquivalenceDataFactory
from .iteration_data.state_pair_data import StatePairDataFactory
from .asp.sketch_asp_factory import SketchASPFactory
from .preprocessing import preprocess_instances


def run(config, data, rng):
    domain_data, instance_datas = preprocess_instances(config)

    i = 0
    selected_instance_idxs = [0]
    largest_unsolved_instance_idx = 0
    timer = CountDownTimer(config.timeout)
    while not timer.is_expired():
        logging.info(f"Iteration: {i}")
        selected_instance_datas = [instance_datas[instance_idx] for instance_idx in selected_instance_idxs]
        print(f"Number of selected instances: {len(selected_instance_datas)}")
        for selected_instance_data in selected_instance_datas:
            print(str(selected_instance_data.instance_filename), selected_instance_data.transition_system.get_num_states())

        # 1.2. Generate feature pool
        state_pair_datas = StatePairDataFactory().make_state_pairs_from_tuple_graphs(selected_instance_datas)
        dlplan_states = []
        for selected_instance_data, state_pair_data in zip(selected_instance_datas, state_pair_datas):
            dlplan_states.extend([selected_instance_data.transition_system.states_by_index[s_idx] for s_idx in state_pair_data.states])
        domain_feature_data = DomainFeatureDataFactory().make_domain_feature_data(config, domain_data, dlplan_states)
        instance_feature_datas = InstanceFeatureDataFactory().make_instance_feature_datas(selected_instance_datas, domain_feature_data)
        rule_equivalence_data, state_pair_equivalence_datas = StatePairEquivalenceDataFactory().make_equivalence_data(state_pair_datas, domain_feature_data, instance_feature_datas)
        tuple_graph_equivalence_datas = TupleGraphEquivalenceDataFactory().make_equivalence_data(selected_instance_datas, state_pair_equivalence_datas)

        # 1.3. Generate asp facts
        is_consistent = False
        consistency_facts = []
        while not is_consistent:
            sketch_asp_factory = SketchASPFactory(config)
            facts = sketch_asp_factory.make_facts(selected_instance_datas, domain_feature_data, rule_equivalence_data, state_pair_equivalence_datas, tuple_graph_equivalence_datas)
            sketch_asp_factory.ground(facts)
            model = sketch_asp_factory.solve()
            sketch_asp_factory.print_statistics()
            sketch = Sketch(DlplanPolicyFactory().make_dlplan_policy_from_answer_set(model, domain_feature_data), config.width)
            all_consistent = True
            for instance_idx, instance_data in enumerate(selected_instance_datas):
                is_instance_consistent, instance_consistency_facts = sketch.verify_consistency(instance_idx, instance_data)
                consistency_facts.extend(instance_consistency_facts)
                if not is_instance_consistent: all_consistent = False
            is_consistent = all_consistent

        logging.info("Learned the following sketch:")
        print(sketch.policy.str())

        # Step 2: try the sketch on all instances until there are
        # (1) either no more instances then we return the sketch, or
        # (2) the sketch fails then we add the instance and do another iteration.
        all_solved = True
        assert all([sketch.solves(instance_data) for instance_data in selected_instance_datas])
        for instance_idx, instance_data in enumerate(instance_datas):
            if not sketch.solves(instance_data):
                all_solved = False
                if instance_idx > largest_unsolved_instance_idx:
                    largest_unsolved_instance_idx = instance_idx
                    selected_instance_idxs = [instance_idx]
                else:
                    selected_instance_idxs.append(instance_idx)
                break
        if all_solved:
            break
        i += 1

    print("Incremental search statistics:")
    print(f"Number of training instances: {len(instance_datas)}")
    print(f"Number of training instances included in the ASP: {len(selected_instance_datas)}")
    print(f"Number of states included in the ASP: {sum([len(instance_data.transition_system.states_by_index) for instance_data in selected_instance_datas])}")
    print(f"Number of features in the pool: {len(domain_feature_data.boolean_features) + len(domain_feature_data.numerical_features)}")
    print(f"Numer of sketch rules: {len(sketch.policy.get_rules())}")
    print(f"Number of selected features: {len(sketch.policy.get_boolean_features()) + len(sketch.policy.get_numerical_features())}")
    print(f"Maximum complexity of selected feature: {max([0] + [boolean_feature.get_boolean().compute_complexity() for boolean_feature in sketch.policy.get_boolean_features()] + [numerical_feature.get_numerical().compute_complexity() for numerical_feature in sketch.policy.get_numerical_features()])}")
    print("Resulting sketch:")
    print(sketch.policy.str())

    return ExitCode.Success, None


def initialize_iteration_data(config, i):
    iteration_dir = config["iterations_dir"] / str(i)
    create_experiment_workspace(iteration_dir, rm_if_existed=True)

    iteration_data = IterationData()
    iteration_data.iteration_dir = iteration_dir
    iteration_data.facts_file = iteration_dir / "facts.lp"
    iteration_data.answer_set_file = iteration_dir / "answer_set.txt"
    iteration_data.output_sketch_file = iteration_dir / "sketch.txt"
    return iteration_data
