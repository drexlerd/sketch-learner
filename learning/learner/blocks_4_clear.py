from learner.src.util.config import EncodingType
from learner.src.util.misc import update_dict
from learner.src.driver import BENCHMARK_DIR


def experiments():
    base = dict(
        pipeline="sketch",
    )

    exps = dict()

    strips_base_blocks_4_clear = update_dict(
        base,
        domain_filename=BENCHMARK_DIR / "blocks_4_clear" / "domain.pddl",
        task_dir=BENCHMARK_DIR / "blocks_4_clear" / "instances",
        task_dir_debug=BENCHMARK_DIR / "blocks_4_clear" / "instances_debug",
    )

    exps["release"] = update_dict(
        strips_base_blocks_4_clear,
        instance_filenames=list(strips_base_blocks_4_clear["task_dir"].iterdir()),
    )

    exps["debug"] = update_dict(
        strips_base_blocks_4_clear,
        instance_filenames=list(strips_base_blocks_4_clear["task_dir_debug"].iterdir()),
        generate_features=False,
        add_boolean_features=[
            "b_nullary(arm-empty)",  # 2
            "b_empty(c_and(c_primitive(clear,0),c_primitive(clear_g,0)))",  # goal separating feature
        ],
        add_numerical_features=[
            "n_count(r_primitive(on,0,1))"
        ],
    )
    return exps
