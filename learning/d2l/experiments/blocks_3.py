
from sketch_learning.util.misc import update_dict


def experiments():
    base = dict(
    )

    exps = dict()

    strips_base = update_dict(
        base,
        domain="domain",
    )

    exps["sketch"] = update_dict(
        strips_base,
        pipeline="sketch_pipeline",
        domain_dir="blocks_3",
        instances=training_instances_4(),
    )

    exps["hierarchy"] = update_dict(
        strips_base,
        pipeline="hierarchy_pipeline",
        domain_dir="blocks_3",
        instances=training_instances_4(),
    )
    return exps


def training_instances_4():
    return [f"p-{i}-{j}" for i in range(2, 5) for j in range(0,200)]
