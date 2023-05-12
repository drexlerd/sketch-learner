from learner.src.util.misc import update_dict
from learner.src.driver import BENCHMARK_DIR


def experiments():
    base = dict(
        pipeline="hierarchy_pipeline",
    )

    exps = dict()

    strips_base = update_dict(
        base,
        domain_filename=BENCHMARK_DIR / "spanner" / "domain.pddl",
        task_dir = BENCHMARK_DIR / "spanner" / "instances",
        task_dir_debug = BENCHMARK_DIR / "spanner" / "instances_debug"
    )

    exps["release"] = update_dict(
        strips_base,
        instance_filenames=list(strips_base["task_dir"].iterdir()),
        add_features=[
            "b_empty(c_some(r_primitive(at,0,1),c_some(r_transitive_closure(r_primitive(link,0,1)),c_some(r_inverse(r_primitive(at,0,1)),c_primitive(man,0)))))",  # deadend feature: stahlberg-et-al-ijcai
        ],
    )

    exps["debug"] = update_dict(
        strips_base,
        instance_filenames=list(strips_base["task_dir_debug"].iterdir()),
        generate_features=False,
        add_features=[
            "n_count(c_and(c_not(c_primitive(tightened,0)),c_some(r_primitive(at,0,1),c_top)))",
            "n_count(c_some(r_primitive(at,0,1),c_all(r_inverse(r_primitive(at,0,1)),c_primitive(man,0))))",
            "n_count(c_some(r_transitive_closure(r_primitive(link,0,1)),c_some(r_inverse(r_primitive(at,0,1)),c_primitive(man,0))))",
            "b_empty(c_some(r_primitive(at,0,1),c_some(r_transitive_closure(r_primitive(link,0,1)),c_some(r_inverse(r_primitive(at,0,1)),c_primitive(man,0)))))",  # deadend feature: stahlberg-et-al-ijcai
            "b_empty(c_and(c_not(c_primitive(tightened,0)),c_primitive(tightened_g,0)))"  # goal separating feature
        ],
    )

    return exps
