from sketch_learning.util.misc import update_dict


def experiments():
    base = dict(
        domain_dir="reward",
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
        debug_features=["n_count(c_not(c_primitive(picked,0)))",  # 3
                        "n_concept_distance(c_primitive(at,0),r_restrict(r_primitive(adjacent,0,1),c_primitive(unblocked,0)),c_diff(c_primitive(picked_g,0),c_primitive(picked,0)))"  # 8
        ],
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
    return [f"instance_{i}x{i}_{j}" for j in range(0, 50) for i in [2, 3]]
