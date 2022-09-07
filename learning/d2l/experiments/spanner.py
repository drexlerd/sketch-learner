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
    return ['p-3-3-3-0', 'p-3-3-3-1', 'p-3-3-3-2', 'p-3-3-3-3', 'p-3-3-3-4', 'p-3-3-3-5', 'p-3-3-3-6', 'p-3-3-3-7', 'p-3-3-3-8', 'p-3-3-3-9', 'p-3-3-3-10', 'p-3-3-3-11', 'p-3-3-3-12', 'p-3-3-3-13', 'p-3-3-3-14', 'p-3-3-3-15', 'p-3-3-3-16', 'p-3-3-3-17', 'p-3-3-3-18', 'p-3-3-3-19', 'p-3-3-4-0', 'p-3-3-4-1', 'p-3-3-4-2', 'p-3-3-4-3', 'p-3-3-4-4', 'p-3-3-4-5', 'p-3-3-4-6', 'p-3-3-4-7', 'p-3-3-4-8', 'p-3-3-4-9', 'p-3-3-4-10', 'p-3-3-4-11', 'p-3-3-4-12', 'p-3-3-4-13', 'p-3-3-4-14', 'p-3-3-4-15', 'p-3-3-4-16', 'p-3-3-4-17', 'p-3-3-4-18', 'p-3-3-4-19', 'p-3-3-5-0', 'p-3-3-5-1', 'p-3-3-5-2', 'p-3-3-5-3', 'p-3-3-5-4', 'p-3-3-5-5', 'p-3-3-5-6', 'p-3-3-5-7', 'p-3-3-5-8', 'p-3-3-5-9', 'p-3-3-5-10', 'p-3-3-5-11', 'p-3-3-5-12', 'p-3-3-5-13', 'p-3-3-5-14', 'p-3-3-5-15', 'p-3-3-5-16', 'p-3-3-5-17', 'p-3-3-5-18', 'p-3-3-5-19', 'p-3-4-4-0', 'p-3-4-4-1', 'p-3-4-4-2', 'p-3-4-4-3', 'p-3-4-4-4', 'p-3-4-4-5', 'p-3-4-4-6', 'p-3-4-4-7', 'p-3-4-4-8', 'p-3-4-4-9', 'p-3-4-4-10', 'p-3-4-4-11', 'p-3-4-4-12', 'p-3-4-4-13', 'p-3-4-4-14', 'p-3-4-4-15', 'p-3-4-4-16', 'p-3-4-4-17', 'p-3-4-4-18', 'p-3-4-4-19', 'p-3-4-5-0', 'p-3-4-5-1', 'p-3-4-5-2', 'p-3-4-5-3', 'p-3-4-5-4', 'p-3-4-5-5', 'p-3-4-5-6', 'p-3-4-5-7', 'p-3-4-5-8', 'p-3-4-5-9', 'p-3-4-5-10', 'p-3-4-5-11', 'p-3-4-5-12', 'p-3-4-5-13', 'p-3-4-5-14', 'p-3-4-5-15', 'p-3-4-5-16', 'p-3-4-5-17', 'p-3-4-5-18', 'p-3-4-5-19', 'p-3-5-5-0', 'p-3-5-5-1', 'p-3-5-5-2', 'p-3-5-5-3', 'p-3-5-5-4', 'p-3-5-5-5', 'p-3-5-5-6', 'p-3-5-5-7', 'p-3-5-5-8', 'p-3-5-5-9', 'p-3-5-5-10', 'p-3-5-5-11', 'p-3-5-5-12', 'p-3-5-5-13', 'p-3-5-5-14', 'p-3-5-5-15', 'p-3-5-5-16', 'p-3-5-5-17', 'p-3-5-5-18', 'p-3-5-5-19', 'p-4-3-3-0', 'p-4-3-3-1', 'p-4-3-3-2', 'p-4-3-3-3', 'p-4-3-3-4', 'p-4-3-3-5', 'p-4-3-3-6', 'p-4-3-3-7', 'p-4-3-3-8', 'p-4-3-3-9', 'p-4-3-3-10', 'p-4-3-3-11', 'p-4-3-3-12', 'p-4-3-3-13', 'p-4-3-3-14', 'p-4-3-3-15', 'p-4-3-3-16', 'p-4-3-3-17', 'p-4-3-3-18', 'p-4-3-3-19', 'p-4-3-4-0', 'p-4-3-4-1', 'p-4-3-4-2', 'p-4-3-4-3', 'p-4-3-4-4', 'p-4-3-4-5', 'p-4-3-4-6', 'p-4-3-4-7', 'p-4-3-4-8', 'p-4-3-4-9', 'p-4-3-4-10', 'p-4-3-4-11', 'p-4-3-4-12', 'p-4-3-4-13', 'p-4-3-4-14', 'p-4-3-4-15', 'p-4-3-4-16', 'p-4-3-4-17', 'p-4-3-4-18', 'p-4-3-4-19', 'p-4-3-5-0', 'p-4-3-5-1', 'p-4-3-5-2', 'p-4-3-5-3', 'p-4-3-5-4', 'p-4-3-5-5', 'p-4-3-5-6', 'p-4-3-5-7', 'p-4-3-5-8', 'p-4-3-5-9', 'p-4-3-5-10', 'p-4-3-5-11', 'p-4-3-5-12', 'p-4-3-5-13', 'p-4-3-5-14', 'p-4-3-5-15', 'p-4-3-5-16', 'p-4-3-5-17', 'p-4-3-5-18', 'p-4-3-5-19', 'p-4-4-4-0', 'p-4-4-4-1', 'p-4-4-4-2', 'p-4-4-4-3', 'p-4-4-4-4', 'p-4-4-4-5', 'p-4-4-4-6', 'p-4-4-4-7', 'p-4-4-4-8', 'p-4-4-4-9', 'p-4-4-4-10', 'p-4-4-4-11', 'p-4-4-4-12', 'p-4-4-4-13', 'p-4-4-4-14', 'p-4-4-4-15', 'p-4-4-4-16', 'p-4-4-4-17', 'p-4-4-4-18', 'p-4-4-4-19', 'p-4-4-5-0', 'p-4-4-5-1', 'p-4-4-5-2', 'p-4-4-5-3', 'p-4-4-5-4', 'p-4-4-5-5', 'p-4-4-5-6', 'p-4-4-5-7', 'p-4-4-5-8', 'p-4-4-5-9', 'p-4-4-5-10', 'p-4-4-5-11', 'p-4-4-5-12', 'p-4-4-5-13', 'p-4-4-5-14', 'p-4-4-5-15', 'p-4-4-5-16', 'p-4-4-5-17', 'p-4-4-5-18', 'p-4-4-5-19', 'p-4-5-5-0', 'p-4-5-5-1', 'p-4-5-5-2', 'p-4-5-5-3', 'p-4-5-5-4', 'p-4-5-5-5', 'p-4-5-5-6', 'p-4-5-5-7', 'p-4-5-5-8', 'p-4-5-5-9', 'p-4-5-5-10', 'p-4-5-5-11', 'p-4-5-5-12', 'p-4-5-5-13', 'p-4-5-5-14', 'p-4-5-5-15', 'p-4-5-5-16', 'p-4-5-5-17', 'p-4-5-5-18', 'p-4-5-5-19', 'p-5-3-3-0', 'p-5-3-3-1', 'p-5-3-3-2', 'p-5-3-3-3', 'p-5-3-3-4', 'p-5-3-3-5', 'p-5-3-3-6', 'p-5-3-3-7', 'p-5-3-3-8', 'p-5-3-3-9', 'p-5-3-3-10', 'p-5-3-3-11', 'p-5-3-3-12', 'p-5-3-3-13', 'p-5-3-3-14', 'p-5-3-3-15', 'p-5-3-3-16', 'p-5-3-3-17', 'p-5-3-3-18', 'p-5-3-3-19', 'p-5-3-4-0', 'p-5-3-4-1', 'p-5-3-4-2', 'p-5-3-4-3', 'p-5-3-4-4', 'p-5-3-4-5', 'p-5-3-4-6', 'p-5-3-4-7', 'p-5-3-4-8', 'p-5-3-4-9', 'p-5-3-4-10', 'p-5-3-4-11', 'p-5-3-4-12', 'p-5-3-4-13', 'p-5-3-4-14', 'p-5-3-4-15', 'p-5-3-4-16', 'p-5-3-4-17', 'p-5-3-4-18', 'p-5-3-4-19', 'p-5-3-5-0', 'p-5-3-5-1', 'p-5-3-5-2', 'p-5-3-5-3', 'p-5-3-5-4', 'p-5-3-5-5', 'p-5-3-5-6', 'p-5-3-5-7', 'p-5-3-5-8', 'p-5-3-5-9', 'p-5-3-5-10', 'p-5-3-5-11', 'p-5-3-5-12', 'p-5-3-5-13', 'p-5-3-5-14', 'p-5-3-5-15', 'p-5-3-5-16', 'p-5-3-5-17', 'p-5-3-5-18', 'p-5-3-5-19', 'p-5-4-4-0', 'p-5-4-4-1', 'p-5-4-4-2', 'p-5-4-4-3', 'p-5-4-4-4', 'p-5-4-4-5', 'p-5-4-4-6', 'p-5-4-4-7', 'p-5-4-4-8', 'p-5-4-4-9', 'p-5-4-4-10', 'p-5-4-4-11', 'p-5-4-4-12', 'p-5-4-4-13', 'p-5-4-4-14', 'p-5-4-4-15', 'p-5-4-4-16', 'p-5-4-4-17', 'p-5-4-4-18', 'p-5-4-4-19', 'p-5-4-5-0', 'p-5-4-5-1', 'p-5-4-5-2', 'p-5-4-5-3', 'p-5-4-5-4', 'p-5-4-5-5', 'p-5-4-5-6', 'p-5-4-5-7', 'p-5-4-5-8', 'p-5-4-5-9', 'p-5-4-5-10', 'p-5-4-5-11', 'p-5-4-5-12', 'p-5-4-5-13', 'p-5-4-5-14', 'p-5-4-5-15', 'p-5-4-5-16', 'p-5-4-5-17', 'p-5-4-5-18', 'p-5-4-5-19', 'p-5-5-5-0', 'p-5-5-5-1', 'p-5-5-5-2', 'p-5-5-5-3', 'p-5-5-5-4', 'p-5-5-5-5', 'p-5-5-5-6', 'p-5-5-5-7', 'p-5-5-5-8', 'p-5-5-5-9', 'p-5-5-5-10', 'p-5-5-5-11', 'p-5-5-5-12', 'p-5-5-5-13', 'p-5-5-5-14', 'p-5-5-5-15', 'p-5-5-5-16', 'p-5-5-5-17', 'p-5-5-5-18', 'p-5-5-5-19']

def training_debug():
    return ["p-3-3-3-19"]