from learner.src.util.misc import update_dict
from learner.src.driver import BENCHMARK_DIR

def experiments():
    base = dict(
    )

    exps = dict()

    strips_base = update_dict(
        base,
        domain_filename=BENCHMARK_DIR / "gripper" / "domain.pddl",
        task_dir=BENCHMARK_DIR / "gripper" / "instances",
    )

    exps["sketch"] = update_dict(
        strips_base,
        pipeline="sketch_pipeline",
        instance_filenames=list(strips_base["task_dir"].iterdir()),
    )

    exps["sketch_debug"] = update_dict(
        strips_base,
        pipeline="sketch_pipeline",
        instance_filenames=list(strips_base["task_dir"].iterdir()),
        generate_features=False,
        add_features=["b_empty(c_some(r_primitive(at_g,0,1),c_primitive(at-robby,0)))",  # 4
                        "b_empty(c_and(c_primitive(at-robby,0),c_one_of(rooma)))",  # robot at room b
                        "b_empty(c_and(c_primitive(at-robby,0),c_one_of(roomb)))",  # robot at room a
                        "n_count(c_some(r_primitive(carry,0,1),c_top))",  # 4 num balls that the robot carries
                        "n_count(r_diff(r_primitive(at_g,0,1), r_primitive(at,0,1)))"  # 4 num misplaced balls, i.e., num balls at roomb
        ],
    )

    exps["hierarchy"] = update_dict(
        strips_base,
        pipeline="hierarchy_pipeline",
        instance_filenames=list(strips_base["task_dir"].iterdir()),
    )

    exps["hierarchy_debug"] = update_dict(
        strips_base,
        pipeline="hierarchy_pipeline",
        instance_filenames=list(strips_base["task_dir"].iterdir()),
        generate_features=False,
        add_features=["b_empty(c_some(r_primitive(at_g,0,1),c_primitive(at-robby,0)))",  # 4
                        "b_empty(c_and(c_primitive(at-robby,0),c_one_of(rooma)))",  # robot at room b
                        "b_empty(c_and(c_primitive(at-robby,0),c_one_of(roomb)))",  # robot at room a
                        "n_count(c_some(r_primitive(carry,0,1),c_top))",  # 4 num balls that the robot carries
                        "n_count(r_diff(r_primitive(at_g,0,1), r_primitive(at,0,1)))"  # 4 num misplaced balls, i.e., num balls at roomb
        ],
    )
    return exps
