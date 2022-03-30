from sketch_learning.util.misc import update_dict


def experiments():
    base = dict(
        domain_dir="miconic",
        pipeline="pipeline",
    )

    exps = dict()

    strips_base = update_dict(
        base,
        domain="domain",
    )

    exps["debug"] = update_dict(
        strips_base,
        instances=training_instances(),
        # for debugging we allow adding features directly into the pipeline
        debug_features=["n_count(c_primitive(boarded,0))",  # 2
                        "n_count(c_some(r_primitive(origin,0,1),c_top))",  # 4
                        "n_count(c_all(r_primitive(origin,0,1),c_primitive(lift-at,0)))",  # 4
                        "n_count(c_and(c_primitive(boarded,0),c_some(r_primitive(destin,0,1),c_primitive(lift-at,0))))"  # 6
        ],
    )

    exps["small_dist"] = update_dict(
        strips_base,
        instances=training_instances(),
        generate_concept_distance_numerical=True
    )

    exps["small"] = update_dict(
        strips_base,
        instances=training_instances(),
    )
    return exps


def training_instances():
    return [f"p-{num_floors}-{num_passengers}-{seed}" for num_floors in range(2,5) for num_passengers in range(2,5) for seed in range(0,100)]
