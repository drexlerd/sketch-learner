# Sketch Learner

## Environment

- Ubuntu 18.04
- Python 3.8.3

## Installation

### Step 1: Clone the repo recursively

```console
git clone --recursive git@github.com:drexlerd/sketch-learner.git
```

### Step 2: Create Python3 virtual environment

```console
python3 -m venv --prompt slearn .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Build Planner Singularity Containers (Testing only)

```console
cd testing/planners
sudo ./build-planners.sh
```

## Running the Learning Experiments


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

## Running the Testing Experiments

```console
cd testing/experiments
./experiment-siwr.py --all
./experiment-dual-bfws.py --all
./experiment-lama-first.py --all
```