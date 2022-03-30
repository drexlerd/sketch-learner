from sketch_learning.util.misc import update_dict


def experiments():
    base = dict(
        domain_dir="delivery",
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
        debug_features=["n_count(r_diff(r_primitive(at_g,0,1),r_primitive(at,0,1)))",  # 4
                        "b_empty(c_primitive(empty,0))",  # 2
                        "n_concept_distance(c_some(r_inverse(r_primitive(at,0,1)), c_primitive(truck,0)), r_primitive(adjacent,0,1), c_primitive(at_g,1))",  # 7
                        "n_concept_distance(c_some(r_inverse(r_primitive(at,0,1)), c_primitive(truck,0)), r_primitive(adjacent,0,1), c_diff(c_some(r_inverse(r_primitive(at,0,1)),c_primitive(package,0)),c_primitive(at_g,1)))",  # 12
        ],
    )

    exps["small_dist"] = update_dict(
        # instances
        strips_base,
        instances=training_instances(),
        generate_concept_distance_numerical=True
    )

    exps["small"] = update_dict(
        # instances
        strips_base,
        instances=training_instances(),
    )
    return exps


def training_instances():
    return [f"instance_2_{j}_{k}" for k in range(0,5) for j in range(1,3)]
