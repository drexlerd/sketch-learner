from sketch_learning.util.misc import update_dict


def experiments():
    base = dict(
        domain_dir="childsnack",
    )

    exps = dict()

    strips_base = update_dict(
        base,
        domain="domain",
    )

    exps["sketch_debug"] = update_dict(
        strips_base,
        pipeline="sketch_pipeline",
        instances=training_instances(),
        debug_features=["n_count(c_and(c_primitive(allergic_gluten,0),c_not(c_primitive(served,0))))",  # 5
                        "n_count(c_and(c_primitive(not_allergic_gluten,0),c_not(c_primitive(served,0))))",  # 5
                        "b_empty(c_and(c_primitive(at_kitchen_sandwich,0), c_primitive(no_gluten_sandwich,0)))",  # 4
                        "b_empty(c_primitive(at_kitchen_sandwich,0))",  # 2
                        "b_empty(c_and(c_primitive(ontray,0),c_primitive(no_gluten_sandwich,0)))",  # 4
                        "b_empty(c_primitive(ontray,0))"],
    )

    exps["sketch"] = update_dict(
        strips_base,
        pipeline="sketch_pipeline",
        instances=training_instances(),
    )

    exps["hierarchy"] = update_dict(
        strips_base,
        pipeline="hierarchy_pipeline",
        instances=training_instances(),
    )
    return exps


def training_instances():
    return [f"p-{children}-{constraintness}-{gluten_factor}-{trays}-{seed}" for children in range(2,6) for constraintness in [1.0] for gluten_factor in [0.0, 0.5, 1.0] for trays in range(1,3) for seed in range(0,5)]
