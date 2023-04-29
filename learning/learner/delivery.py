from learner.src.util.misc import update_dict
from learner.src.driver import BENCHMARK_DIR


def experiments():
    base = dict(
    )

    exps = dict()

    strips_base = update_dict(
        base,
        domain_filename=BENCHMARK_DIR / "delivery" / "domain.pddl",
        task_dir=BENCHMARK_DIR / "delivery" / "instances",
    )

    exps["sketch"] = update_dict(
        strips_base,
        pipeline="sketch_pipeline",
        instance_filenames=list(strips_base["task_dir"].iterdir()),
    )

    exps["sketch_debug"] = update_dict(
        strips_base,
        pipeline="sketch_pipeline",
        instance_filenames=list(strips_base["task_dir"].iterdir()),
        generate_features=False,
        add_features=["n_count(c_not(c_equal(r_primitive(at_g,0,1),r_primitive(at,0,1))))",  # 5
                        "b_empty(c_primitive(empty,0))",  # 2
                        "n_concept_distance(c_some(r_inverse(r_primitive(at,0,1)),c_primitive(truck,0)),r_primitive(adjacent,0,1),c_some(r_inverse(r_primitive(at_g,0,1)),c_top))",  # 10
                        "n_concept_distance(c_some(r_inverse(r_primitive(at,0,1)),c_primitive(truck,0)), r_primitive(adjacent,0,1), c_and(c_all(r_inverse(r_primitive(at_g,0,1)),c_bot),c_some(r_inverse(r_primitive(at,0,1)),c_primitive(package,0))))",  # 15
        ],
    )

    exps["hierarchy"] = update_dict(
        strips_base,
        pipeline="hierarchy_pipeline",
        instance_filenames=list(strips_base["task_dir"].iterdir()),
    )

    exps["hierarchy_debug"] = update_dict(
        strips_base,
        pipeline="hierarchy_pipeline",
        instance_filenames=list(strips_base["task_dir"].iterdir()),
        generate_features=False,
        add_features=["n_count(c_not(c_equal(r_primitive(at_g,0,1),r_primitive(at,0,1))))",  # 5
                      "n_count(r_diff(r_primitive(at_g,0,1),r_primitive(at,0,1)))",  # goal separating feature
                      "b_empty(c_primitive(empty,0))",  # 2
                      "n_concept_distance(c_some(r_inverse(r_primitive(at,0,1)),c_primitive(truck,0)),r_primitive(adjacent,0,1),c_some(r_inverse(r_primitive(at_g,0,1)),c_top))",  # 10
                      "n_concept_distance(c_some(r_inverse(r_primitive(at,0,1)),c_primitive(truck,0)), r_primitive(adjacent,0,1), c_and(c_all(r_inverse(r_primitive(at_g,0,1)),c_bot),c_some(r_inverse(r_primitive(at,0,1)),c_primitive(package,0))))"  # 15
        ],
    )
    return exps
