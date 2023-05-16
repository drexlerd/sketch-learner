from learner.src.util.misc import update_dict
from learner.src.driver import BENCHMARK_DIR

def experiments():
    base = dict(
        pipeline="sketch",
    )

    exps = dict()

    strips_base = update_dict(
        base,
        domain_filename=BENCHMARK_DIR / "gripper" / "domain.pddl",
        task_dir=BENCHMARK_DIR / "gripper" / "instances",
        task_dir_debug=BENCHMARK_DIR / "gripper" / "instances_debug",
    )

    exps["release"] = update_dict(
        strips_base,
        instance_filenames=list(strips_base["task_dir"].iterdir()),
    )

    exps["debug"] = update_dict(
        strips_base,
        instance_filenames=list(strips_base["task_dir_debug"].iterdir()),
        generate_features=False,
        add_features=["b_empty(c_and(c_primitive(at-robby,0),c_one_of(rooma)))",  # robot at room b
                      "n_count(r_primitive(carry,0,1))",  # 4 num balls that the robot carries
                      "n_count(r_diff(r_primitive(at_g,0,1), r_primitive(at,0,1)))",  # 4 num misplaced balls, i.e., num balls at roomb
                      "b_empty(r_diff(r_primitive(at_g,0,1), r_primitive(at,0,1)))",  # goal separating feature
        ],
    )
    return exps
