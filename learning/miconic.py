from learner.src.defaults import EncodingType
from learner.src.util.misc import update_dict
from learner.src.driver import BENCHMARK_DIR


def experiments():
    base = dict(
        pipeline="sketch",
    )

    exps = dict()

    strips_base = update_dict(
        base,
        domain_filename=BENCHMARK_DIR / "miconic" / "domain.pddl",
        task_dir=BENCHMARK_DIR / "miconic" / "instances",
        task_dir_debug=BENCHMARK_DIR / "miconic" / "instances_debug",
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
            "b_empty(c_and(c_not(c_primitive(served,0)),c_primitive(served_g,0)))",  # goal separating feature
        ],
        add_numerical_features=[
            "n_count(c_primitive(served,0))",
            "n_count(c_primitive(boarded,0))",
            "n_count(c_and(c_primitive(boarded,0),c_some(r_primitive(destin,0,1),c_primitive(lift-at,0))))",
            "n_count(c_some(r_primitive(origin,0,1),c_primitive(lift-at,0)))",
        ],

    )
    return exps
