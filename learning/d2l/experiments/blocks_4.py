from sketch_learning.util.misc import update_dict


def experiments():
    base = dict(
        pipeline="pipeline",
    )

    exps = dict()

    strips_base = update_dict(
        base,
        domain="domain",
    )

    exps["debug"] = update_dict(
        # instances
        strips_base,
        domain_dir="blocks_4",
        instances=training_instances_4(),
        # for debugging we allow adding features directly into the pipeline
        debug_features=["n_count(c_primitive(clear,0))",  # 2
                        "n_count(c_all(r_transitive_closure(r_primitive(on,0,1)),c_equal(r_primitive(on_g,0,1),r_primitive(on,0,1))))",  # 7
                        "n_count(c_equal(r_primitive(on_g,0,1),r_primitive(on,0,1)))",  # 4
                        "b_empty(c_primitive(holding,0))"
                        ],  # 2
    )

    exps["small"] = update_dict(
        # instances
        strips_base,
        domain_dir="blocks_4",
        instances=training_instances_4(),
    )

    exps["clear"] = update_dict(
        # imnstances
        strips_base,
        domain_dir="blocks_4_clear",
        instances=training_instances_4(),
    )

    exps["on"] = update_dict(
        # imnstances
        strips_base,
        domain_dir="blocks_4_on",
        instances=["p-3-0"],
    )
    return exps


def training_instances_4():
    return [f"p-{i}-{j}" for i in range(3, 6) for j in range(0,200)]
