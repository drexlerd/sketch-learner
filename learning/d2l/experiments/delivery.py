from sketch_learning.util.misc import update_dict


def experiments():
    base = dict(
        domain_dir="delivery",
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
        debug_features=["n_count(c_not(c_equal(r_primitive(at_g,0,1),r_primitive(at,0,1))))",  # 5
                        "b_empty(c_primitive(empty,0))",  # 2
                        "n_concept_distance(c_some(r_inverse(r_primitive(at,0,1)),c_primitive(truck,0)), r_primitive(adjacent,0,1), c_primitive(at_g,1))",  # 7
                        "n_concept_distance(c_some(r_inverse(r_primitive(at,0,1)),c_primitive(truck,0)), r_primitive(adjacent,0,1), c_and(c_all(r_inverse(r_primitive(at_g,0,1)),c_bot),c_some(r_inverse(r_primitive(at,0,1)),c_primitive(package,0))))",  # 12
        ],
    )

    exps["sketch"] = update_dict(
        strips_base,
        pipeline="sketch_pipeline",
        instances=training_instances(),
    )

    exps["sketch_dist"] = update_dict(
        strips_base,
        pipeline="sketch_pipeline",
        instances=training_instances(),
        generate_concept_distance_numerical=True
    )

    exps["hierarchy"] = update_dict(
        strips_base,
        pipeline="hierarchy_pipeline",
        instances=training_instances(),
    )

    exps["hierarchy_dist"] = update_dict(
        strips_base,
        pipeline="hierarchy_pipeline",
        instances=training_instances(),
        generate_concept_distance_numerical=True
    )
    return exps


def training_instances():
    return [f"instance_{i}_{j}_{k}" for i in range(2,4) for j in range(1,3) for k in range(0,10) ]
