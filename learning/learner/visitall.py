from learner.src.util.misc import update_dict
from learner.src.driver import BENCHMARK_DIR


def experiments():
    base = dict(
        domain_dir="visitall",
    )

    exps = dict()

    strips_base = update_dict(
        base,
        domain_filename=BENCHMARK_DIR / "visitall" / "domain.pddl",
        task_dir = BENCHMARK_DIR / "visitall" / "instances"
    )

    exps["sketch_debug"] = update_dict(
        strips_base,
        pipeline="sketch_pipeline",
        instance_filenames=list(strips_base["task_dir"].iterdir()),
        generate_features=False,
        add_features=["n_count(c_not(c_primitive(visited,0)))",  # 3
                      "n_concept_distance(c_primitive(at-robot,0),r_primitive(connected,0,1),c_not(c_primitive(visited,0)))",  # 5
                      "n_concept_distance(c_primitive(at-robot,0),r_primitive(connected,0,1),c_not(c_all(r_restrict(r_primitive(connected,0,1),c_primitive(visited_g,0)),c_primitive(visited,0))))",
                      "b_empty(c_and(c_not(c_primitive(visited,0)),c_primitive(visited_g,0)))",  # goal separating feature
        ],
    )

    exps["sketch"] = update_dict(
        strips_base,
        pipeline="sketch_pipeline",
        instance_filenames=list(strips_base["task_dir"].iterdir()),
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
        add_features=["n_count(c_not(c_primitive(visited,0)))",  # 3
                      "n_concept_distance(c_primitive(at-robot,0),r_primitive(connected,0,1),c_not(c_primitive(visited,0)))",  # 5
                      "n_concept_distance(c_primitive(at-robot,0),r_primitive(connected,0,1),c_not(c_all(r_restrict(r_primitive(connected,0,1),c_primitive(visited_g,0)),c_primitive(visited,0))))",
                      "b_empty(c_and(c_not(c_primitive(visited,0)),c_primitive(visited_g,0)))",  # goal separating feature
        ],
    )

    return exps
