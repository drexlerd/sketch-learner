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

The following command prints the help message.

```console
python3 learning/main.py --help
```

The following command, learns a sketch of width 1 for a set of planning problem over a common domain.

```console
python3 learning/main.py --domain_filepath <path/to/pddl/domain> --problems_directory <path/to/pddl/problems> --workspace <path/to/workspace> --width 1
```

It is important that the planning problems are small. If you have a problem generator, then exhaustively generate small instances with the number of each object type in the range from 1 to 3.


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