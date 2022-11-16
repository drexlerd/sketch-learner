from sketch_learning.util.misc import update_dict


def experiments():
    base = dict(
        domain_dir="spanner",
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
        debug_features=["n_count(c_and(c_primitive(tightened_g,0),c_not(c_primitive(tightened,0))))",  # 4
                        "n_count(r_primitive(at,0,1))",  # 2
                        "b_empty(c_some(r_primitive(at,0,1),c_all(r_inverse(r_primitive(at,0,1)),c_primitive(man,0)))))"  # 7
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
    # return ["p-3-3-3-1", "p-3-3-3-16"]
    return [f"p-{i}-{j}-{k}-{seed}" for i in range(3,6) for j in range(3,6) for k in range(3,6) for seed in range(20)]
