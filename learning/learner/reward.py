from learner.src.util.misc import update_dict
from learner.src.driver import BENCHMARK_DIR


def experiments():
    base = dict(
        pipeline="sketch",
    )

    exps = dict()

    strips_base = update_dict(
        base,
        domain_filename=BENCHMARK_DIR / "reward" / "domain.pddl",
        task_dir = BENCHMARK_DIR / "reward" / "instances",
        task_dir_debug = BENCHMARK_DIR / "reward" / "instances_debug"
    )

    exps["release"] = update_dict(
        strips_base,
        instance_filenames=list(strips_base["task_dir"].iterdir()),
    )

    exps["debug"] = update_dict(
        strips_base,
        instance_filenames=list(strips_base["task_dir_debug"].iterdir()),
        generate_features=False,
        add_boolean_features=[
            "b_empty(c_primitive(reward,0))"  # goal separating feature
        ],
        add_numerical_features=[
            "n_count(c_primitive(reward,0))",
            "n_concept_distance(c_primitive(at,0),r_restrict(r_primitive(adjacent,0,1),c_primitive(unblocked,0)),c_primitive(reward,0))",
        ],

    )

    return exps
