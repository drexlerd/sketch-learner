from sketch_learning.util.misc import update_dict


def experiments():
    base = dict(
        domain_dir="reward",
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
        debug_features=["n_count(c_not(c_primitive(picked,0)))",  # 3
                        "n_concept_distance(c_primitive(at,0),r_restrict(r_primitive(adjacent,0,1),c_primitive(unblocked,0)),c_diff(c_primitive(picked_g,0),c_primitive(picked,0)))"  # 8
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
    return [f"instance_{i}x{i}_{j}" for j in range(0, 50) for i in [2, 3]]
