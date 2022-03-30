from sketch_learning.util.misc import update_dict


def experiments():
    base = dict(
        domain_dir="gripper",
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
        debug_features=["b_empty(c_some(r_primitive(at_g,0,1),c_primitive(at-robby,0)))",  # 4
                        "n_count(c_some(r_primitive(carry,0,1),c_top))",  # 4
                        "n_count(r_diff(r_primitive(at_g,0,1), r_primitive(at,0,1)))"  # 4
        ],
    )

    exps["small"] = update_dict(
        strips_base,
        instances=training_instances(),
    )

    exps["single"] = update_dict(
        strips_base,
        instances=['p-2-0'],
    )
    return exps


def training_instances():
    return ['p-1-0', 'p-2-0', 'p-3-0', 'p-4-0', 'p-5-0']
