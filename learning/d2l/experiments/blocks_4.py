
from sketch_learning.util.misc import update_dict


def experiments():
    base = dict(
    )

    exps = dict()

    strips_base = update_dict(
        base,
        domain="domain",
    )

    exps["sketch_debug"] = update_dict(
        strips_base,
        pipeline="sketch_pipeline",
        domain_dir="blocks_4",
        instances=training_instances_4(),
        debug_features=["n_count(c_primitive(clear,0))",  # 2
                        "n_count(c_all(r_transitive_closure(r_primitive(on,0,1)),c_equal(r_primitive(on_g,0,1),r_primitive(on,0,1))))",  # 7
                        "n_count(c_equal(r_primitive(on_g,0,1),r_primitive(on,0,1)))",  # 4
                        "b_empty(c_primitive(holding,0))"
                        ],  # 2
    )

    exps["sketch"] = update_dict(
        strips_base,
        pipeline="sketch_pipeline",
        domain_dir="blocks_4",
        instances=training_instances_4(),
    )

    exps["sketch_clear"] = update_dict(
        strips_base,
        pipeline="sketch_pipeline",
        domain_dir="blocks_4_clear",
        instances=training_instances_4_fixed_goal(),
    )

    exps["sketch_on"] = update_dict(
        strips_base,
        pipeline="sketch_pipeline",
        domain_dir="blocks_4_on",
        instances=training_instances_4_fixed_goal(),
        #debug_features=["n_count(r_and(r_primitive(on_g,0,1), r_primitive(on,0,1)))",  # 4
        #],
    )

    exps["hierarchy"] = update_dict(
        strips_base,
        pipeline="hierarchy_pipeline",
        domain_dir="blocks_4",
        instances=training_instances_4(),
    )

    exps["hierarchy_clear"] = update_dict(
        strips_base,
        pipeline="hierarchy_pipeline",
        domain_dir="blocks_4_clear",
        instances=training_instances_4_fixed_goal(),
    )

    exps["hierarchy_on"] = update_dict(
        strips_base,
        pipeline="hierarchy_pipeline",
        domain_dir="blocks_4_on",
        instances=training_instances_4_fixed_goal(),
    )
    return exps


def training_instances_4():
    return [f"p-{i}-{j}" for i in range(2, 5) for j in range(0,200)]

def training_instances_4_fixed_goal():
    """ For fixed goal we do not need to use random seeds. """
    return [f"p-{i}-0" for i in range(2, 5)]
