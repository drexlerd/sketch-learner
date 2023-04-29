from learner.src.util.misc import update_dict
from learner.src.driver import BENCHMARK_DIR


def experiments():
    base = dict(
    )

    exps = dict()

    strips_base_blocks_4 = update_dict(
        base,
        domain_filename=BENCHMARK_DIR / "blocks_4" / "domain.pddl",
        task_dir=BENCHMARK_DIR / "blocks_4" / "instances",
    )

    strips_base_blocks_4_clear = update_dict(
        base,
        domain_filename=BENCHMARK_DIR / "blocks_4_clear" / "domain.pddl",
        task_dir=BENCHMARK_DIR / "blocks_4_clear" / "instances",
    )

    strips_base_blocks_4_on = update_dict(
        base,
        domain_filename=BENCHMARK_DIR / "blocks_4_on" / "domain.pddl",
        task_dir=BENCHMARK_DIR / "blocks_4_on" / "instances",
    )

    exps["sketch_debug"] = update_dict(
        strips_base_blocks_4,
        pipeline="sketch_pipeline",
        domain_dir="blocks_4",
        instance_filenames=list(strips_base_blocks_4["task_dir"].iterdir()),
        generate_features=False,
        add_features=["n_count(c_primitive(clear,0))",  # 2
                      "n_count(c_all(r_transitive_closure(r_primitive(on,0,1)),c_equal(r_primitive(on_g,0,1),r_primitive(on,0,1))))",  # 7
                      "n_count(c_equal(r_primitive(on_g,0,1),r_primitive(on,0,1)))",  # 4
                      "n_count(r_and(r_primitive(on_g,0,1),r_primitive(on,0,1)))",  # 4
                      "n_count(r_primitive(on,0,1))",  # 2
                      "b_empty(c_primitive(holding,0))",  # 2
                      "n_count(c_and(c_equal(r_primitive(on,0,1),r_primitive(on_g,0,1)),c_not(c_primitive(holding,0))))",  # 7
                      "b_nullary(arm-empty)",  # 2
                      "n_count(c_some(r_transitive_closure(r_primitive(on,0,1)),c_some(r_inverse(r_primitive(on,0,1)),c_top)))"  # 7
        ],
        max_num_rules=6,
    )

    exps["sketch"] = update_dict(
        strips_base_blocks_4,
        pipeline="sketch_pipeline",
        domain_dir="blocks_4",
        instance_filenames=list(strips_base_blocks_4["task_dir"].iterdir()),
    )

    exps["sketch_clear"] = update_dict(
        strips_base_blocks_4_clear,
        pipeline="sketch_pipeline",
        domain_dir="blocks_4_clear",
        instance_filenames=list(strips_base_blocks_4_clear["task_dir"].iterdir()),
    )

    exps["sketch_on"] = update_dict(
        strips_base_blocks_4_on,
        pipeline="sketch_pipeline",
        domain_dir="blocks_4_on",
        instance_filenames=list(strips_base_blocks_4_on["task_dir"].iterdir()),
    )

    exps["hierarchy"] = update_dict(
        strips_base_blocks_4,
        pipeline="hierarchy_pipeline",
        domain_dir="blocks_4",
        instance_filenames=list(strips_base_blocks_4["task_dir"].iterdir()),
    )

    exps["hierarchy_clear"] = update_dict(
        strips_base_blocks_4_clear,
        pipeline="hierarchy_pipeline",
        domain_dir="blocks_4_clear",
        instance_filenames=list(strips_base_blocks_4_clear["task_dir"].iterdir()),
    )

    exps["hierarchy_on"] = update_dict(
        strips_base_blocks_4_on,
        pipeline="hierarchy_pipeline",
        domain_dir="blocks_4_on",
        instance_filenames=list(strips_base_blocks_4_on["task_dir"].iterdir()),

    )

    exps["hierarchy_on_debug"] = update_dict(
        strips_base_blocks_4_on,
        pipeline="hierarchy_pipeline",
        domain_dir="blocks_4_on",
        instance_filenames=list(strips_base_blocks_4_on["task_dir"].iterdir()),
        generate_features=False,
        add_features=["b_nullary(arm-empty)",  # 2
                      "n_count(c_primitive(clear,0))",  # 2
                      "n_count(c_and(c_primitive(clear,0),c_one_of(b1)))",  # 4
                      "n_count(c_some(r_primitive(on,0,1),c_one_of(b2)))",  # 4
                      "b_empty(c_and(c_one_of(b1),c_some(r_primitive(on,0,1),c_one_of(b2))))",  # 6
                      "n_count(c_some(r_transitive_closure(r_primitive(on,0,1)),c_one_of(b1)))",
                      "n_count(c_some(r_transitive_closure(r_primitive(on,0,1)),c_one_of(b2)))",
                      "n_count(c_equal(r_primitive(on_g,0,1),r_primitive(on,0,1)))",  # 4
                      "n_count(r_primitive(on,0,1))",  # 2
                      "n_count(c_and(c_equal(r_primitive(on,0,1),r_primitive(on_g,0,1)),c_not(c_primitive(holding,0))))",  # 7
                      "n_count(c_primitive(on-table,0))"  # 2
        ],
        # works with delta=4, max_num_rules=4, and without goal separating feature
    )
    return exps
