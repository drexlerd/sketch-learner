from sketch_learning.util.misc import update_dict


def experiments():
    base = dict(
        domain_dir="childsnack",
        pipeline="pipeline",
        test_instances=[],
    )

    exps = dict()

    strips_base = update_dict(
        base,
        domain="domain",
    )

    exps["debug"] = update_dict(
        # instances
        strips_base,
        instances=training_instances(),
        # for debugging we allow adding features directly into the pipeline
        debug_features=["n_count(c_and(c_primitive(allergic_gluten,0),c_not(c_primitive(served,0))))",  # 5
                        "n_count(c_and(c_primitive(not_allergic_gluten,0),c_not(c_primitive(served,0))))",  # 5
                        "b_empty(c_and(c_primitive(at_kitchen_sandwich,0), c_primitive(no_gluten_sandwich,0)))",  # 4
                        "b_empty(c_primitive(at_kitchen_sandwich,0))",  # 2
                        "b_empty(c_and(c_primitive(ontray,0),c_primitive(no_gluten_sandwich,0)))",  # 4
                        "b_empty(c_primitive(ontray,0))"],
    )

    exps["small"] = update_dict(
        # instances
        strips_base,
        instances=training_instances(),
    )
    return exps


def training_instances():
    return [f"p-{children}-{constraintness}-{gluten_factor}-{trays}-{seed}" for children in range(2,6) for constraintness in [1.0] for gluten_factor in [0.0, 0.5, 1.0] for trays in range(1,3) for seed in range(0,5)]
