# Sketch Learner

This repository contains code for learning policy sketches for a given set of training instances Q_Train from a class of problems Q over a common classical planning domain.

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

Running the learning experiments requires setting the environment variable `SKETCH_LEARNER_DIR` to the location of the root of the repo.
The experiments can be run in a slurm environment by running the following sequence of commands.

```console
cd learning/experiments/scripts

./run_all_tractable.sh
./run_all_ipc2023.sh
```

## Running the Testing Experiments (ICAPS2022)

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

