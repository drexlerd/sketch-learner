# Sketch-Learner

## Installation

### Step 1: Cloning the repo recursively

```console
git clone --recursive git@github.com:drexlerd/sketch-learner.git
```

### Step 2: Build singularity containers

```console
sudo ./build-singularities.sh
```

### Step 3: Create Python3 virtual environment

```console
python3 -m venv --prompt slearn .venv
pip install -r requirements.txt
```

### Step 3: Export environment variables

```console
export D2L_PATH="<root>/learner/d2l"
export PYTHONPATH="<root>/learner/d2l/src"
```
