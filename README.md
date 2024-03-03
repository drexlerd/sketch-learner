# Sketch Learner

## Environment

- Ubuntu 18.04
- Python 3.8.3

## Installation

### Step 1: Clone the repo

```console
git clone git@github.com:drexlerd/sketch-learner.git
```

### Step 2: Create Python3 virtual environment

```console
python3 -m venv --prompt slearn .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## How to learn sketches for a new planning domain?

The following command, learns a sketch of width 1 for a set of planning problem over a common domain.

```console
python3 learner/learning/main.py --domain <path/to/pddl/domain> --task_dir <path/to/pddl/problems> --width 1
```

It is important that the planning problems are small. If you have a problem generator, then exhaustively generate small instances with the number of each object type in the range from 1 to 3.

If you want to change hyperparameters, or get a deeper understanding of your planning domain, by finding suitable features and learning a sketch for a fixed set of features, or just for debugging purposes, you can create an domain specific experiment script, e.g., a python script for Gripper can look as follows.

```python
from learner.src.util.config import EncodingType
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

    exps["debug"] = update_dict(
        strips_base,
        generate_features=False,
        add_boolean_features=[
            "b_empty(c_and(c_primitive(at-robby,0),c_one_of(rooma)))",  # robot at room b
            "b_empty(r_diff(r_primitive(at_g,0,1), r_primitive(at,0,1)))",  # goal separating feature
        ],
        add_numerical_features=[
            "n_count(r_primitive(carry,0,1))",  # 4 num balls that the robot carries
            "n_count(r_diff(r_primitive(at_g,0,1), r_primitive(at,0,1)))",  # 4 num misplaced balls, i.e., num balls at roomb
        ],
    )
    return exps
```

In this file, we define two experiments. The `debug` experiment turns of the feature generator and adds handcrafted domain specific features. You can also modify other hyperparameters from the [list of default parameters](https://github.com/drexlerd/sketch-learner/blob/main/learning/learner/src/util/defaults.py). You can additionally pass this script to the call as follows.

```console
python3 learner/learning/main.py --domain <path/to/pddl/domain> --task_dir <path/to/pddl/problems> --width 1 --exp_id gripper:debug
```


## Running the Learning Experiments (ICAPS2022)


```console
cd learning/experiments/scripts

./blocks_4_clear_0.sh
./blocks_4_clear_1.sh
./blocks_4_clear_2.sh

./blocks_4_on_0.sh
./blocks_4_on_1.sh
./blocks_4_on_2.sh

./delivery_0.sh
./delivery_1.sh
./delivery_2.sh

./gripper_0.sh
./gripper_1.sh
./gripper_2.sh

./miconic_0.sh
./miconic_1.sh
./miconic_2.sh

./reward_0.sh
./reward_1.sh
./reward_2.sh

./spanner_0.sh
./spanner_1.sh
./spanner_2.sh

./visitall_0.sh
./visitall_1.sh
./visitall_2.sh
```

## Running the Testing Experiments (ICAPS2022)

TODO

Build the planner apptainers

```console
cd testing/planners
./build-planners.sh
```

Run the experiments

```console
cd testing/experiments
./experiment-siwr.py --all
./experiment-dual-bfws.py --all
./experiment-lama-first.py --all
```