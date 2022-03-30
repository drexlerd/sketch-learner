from sketch_learning.util.misc import update_dict


def experiments():
    base = dict(
        domain_dir="visitall",
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
        debug_features=["n_count(c_not(c_primitive(visited,0)))",  # 3
                        "n_concept_distance(c_primitive(at-robot,0),r_primitive(connected,0,1),c_not(c_primitive(visited,0)))",  # 5
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
    return [f"p-{unavail}-{pct}-{grid_size}-{seed}" for unavail in range(1,3) for pct in [0.5,1.0] for grid_size in range(2,4) for seed in range(0,50) ]
