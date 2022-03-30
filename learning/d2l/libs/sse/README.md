
SSE - State Space Expansion for Classical Planning Problems
====================================

SSE is a port of the [FS planner](https://github.com/aig-upf/fs) customized to perform
one single task: expand the reachable state space of any input classical planning problem
and output different kinds of relevant information such as the logical composition of
states or the state space transitions.

SSE strives to be compatible with containerization technologies;
at the moment, we support [Docker](https://www.docker.com/) and [Singularity](https://sylabs.io/singularity/).

## Docker

In order to build or run the Docker image, you need to
[have Docker installed on your machine](https://docs.docker.com/engine/installation).

## Building the Docker image

Build the docker image with the following command from the repo root:
```shell script
sudo docker build -t sse -f containers/Dockerfile .
```

## Using the Docker image

You can open a terminal on the image for inspection or debugging by running
```shell script
sudo docker run --entrypoint bash -it sse
```

Now, if you want to expand the full state space of a planning problem located on the `$DOWNWARD_BENCHMARKS` directory
of your host machine, you need to run:

```shell script
sudo docker run --rm -v $DOWNWARD_BENCHMARKS:/benchmarks sse --instance /benchmarks/gripper/prob01.pddl
```


This mounts the `$DOWNWARD_BENCHMARKS` directory of your host machine under the container directory `/benchmarks`,
which is the place where the containerized planner looks for the problem.
The path stored in the `$DOWNWARD_BENCHMARKS` variable must be absolute.

If the name of the PDDL domain is not obvious (e.g., is not "domain.pddl" or similar), you'll need
to specify it as well:

```shell script
sudo docker run --rm -v $DOWNWARD_BENCHMARKS:/benchmarks sse \
    --domain /benchmarks/gripper/domain.pddl \
    --instance /benchmarks/gripper/prob01.pddl
```

## Singularity

A ready-to-use singularity image can be built **from the Docker image described above**
(meaning: you will need to have built the Docker image before attempting this),
as follows:

```shell script
sudo singularity build sse.sif docker-daemon://sse:latest
```

You can run the image **without sudo** as a normal binary, but in order not to affect performance, it's better
if you run the image as read-only, and give the planner a local directory **outside the Singularty container**
where it can leave intermediate files (see the use of `/tmp/workspace` below):
```shell script
./sse.sif --workspace /tmp/workspace \
          --domain $DOWNWARD_BENCHMARKS/gripper/domain.pddl \
          --instance $DOWNWARD_BENCHMARKS/gripper/prob01.pddl
```

To start a container with an interactive shell, you need to:
```shell script
singularity shell sse.sif
```

## Command-Line Options

These are some of the relevant command-line options.
Top-level options:

```shell script
--instance <instance_filename>
--domain <domain_filename> 
--workspace <directory_filename>  # Use some local scratch filesystem, maybe even temporary, when running on a cluster
--options "<comma-separated-list-of-options>"
```

Options is a string with a list of comma-separated options.
Each option is a pair <key>=<value>. Boolean options are specified by using strings "true" and "false".
The options are:
* `max_nodes_per_class=<n>`: How many nodes at most we want to print for each class (dead, non-dead). 
Nodes will be selected randomly (default: print all nodes in each class). Default: all nodes.
* `ignore_non_fringe_dead_states=true|false`: Whether to ignore non-fringe unsolvable states. 
An unsolvable state is "on the fringe" if it is the successor of at least one alive state. Default: true.
* `print_transitions=true|false`: Whether to print a string "(E) x y" for each transition between states with IDs x and y. Default: true.
* `seed=<n>`: The seed for the RNG used to randomize the printed nodes of each class, if necessary. Default: 1.

To illustrate, this would be a typical invocation:

```shell script
./sse.sif --workspace /tmp/workspace \
          --instance $DOWNWARD_BENCHMARKS/gripper/prob01.pddl \
          --options max_nodes_per_class=100,ignore_non_fringe_dead_states=true,seed=15
```

