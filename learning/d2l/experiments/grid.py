from sketch_learning.util.misc import update_dict


def experiments():
    base = dict(
        domain_dir="grid",
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
        debug_features=["n_count(c_primitive(locked,0))",  # 2
                        "n_count(r_diff(r_primitive(at_g,0,1),r_primitive(at,0,1)))",  # 4
                        "b_empty(c_and(c_primitive(holding,0), c_some(r_primitive(key-shape,0,1),c_some(r_inverse(r_primitive(lock-shape,0,1)),c_primitive(locked,0)))))",  # 9
                        "b_empty(c_and(c_primitive(holding,0), c_projection(r_diff(r_primitive(at_g,0,1),r_primitive(at,0,1)), 0)))",  # 7
                        "b_empty(holding(0))"
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
    return [f"p-{keys_locks}-{keys_locks}-{prob_key_in_goal}-{shapes}-{x}-{y}-{seed}" for keys_locks in ["0", "1", "2"] for prob_key_in_goal in [0,50,100] for shapes in [1] for x in [2] for y in [2] for seed in range(0, 50)] + \
           [f"p-{keys_locks}-{keys_locks}-{prob_key_in_goal}-{shapes}-{x}-{y}-{seed}" for keys_locks in ["20", "02", "11"] for prob_key_in_goal in [0,50,100] for shapes in [2] for x in [2] for y in [2] for seed in range(0, 50)]
