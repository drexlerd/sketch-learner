#! /usr/bin/env python

"""
Example experiment for the FF planner
(http://fai.cs.uni-saarland.de/hoffmann/ff.html).
"""

import os
import platform
import re

from downward import suites
from downward.reports.absolute import AbsoluteReport
from lab.environments import TetralithEnvironment, BaselSlurmEnvironment, LocalEnvironment
from lab.experiment import Experiment
from lab.reports import Attribute, geometric_mean


# Create custom report class with suitable info and error attributes.
class BaseReport(AbsoluteReport):
    INFO_ATTRIBUTES = ["time_limit", "memory_limit"]
    ERROR_ATTRIBUTES = [
        "domain",
        "problem",
        "algorithm",
        "unexplained_errors",
        "error",
        "node",
    ]

NODE = platform.node()
REMOTE = re.match(r"tetralith\d+.nsc.liu.se|n\d+", NODE)
BENCHMARKS_DIR = "../benchmarks"
if REMOTE:
    ENV = TetralithEnvironment(
        partition="tetralith",
        email="",
        memory_per_cpu="3G",
        cpus_per_task=16,
        setup=TetralithEnvironment.DEFAULT_SETUP,
        extra_options="#SBATCH --account=snic2021-5-330")
    SUITE = ["barman", "blocksworld_3", "blocksworld_4", "childsnack", "delivery", "gripper", "miconic", "reward", "spanner", "visitall"]
    SUITE = ["blocksworld_3:p-3-0.pddl", "childsnack:p-2-1.0-0.0-1-0.pddl", "delivery:instance_2_1_0.pddl", "delivery:instance_2_2_0.pddl", "gripper:p-1-0.pddl", "gripper:p-2-0.pddl", "miconic:p-2-2-0.pddl", "miconic:p-3-3-0.pddl", "reward", "visitall"]
    SUITE = ["blocksworld_3:p-3-0.pddl", "childsnack:p-2-1.0-0.0-1-0.pddl", "delivery:instance_2_1_0.pddl", "delivery:instance_2_2_0.pddl", "gripper:p-1-0.pddl", "gripper:p-2-0.pddl", "miconic:p-2-2-0.pddl", "miconic:p-3-3-0.pddl", "reward", "visitall"]
    TIME_LIMIT = 3 * 3600
else:
    ENV = LocalEnvironment(processes=1)
    SUITE = ["visitall:p-1-0.5-2-0.pddl"]
    SUITE = ["blocksworld_3:p-3-0.pddl", "childsnack:p-2-1.0-0.0-1-0.pddl", "delivery:instance_2_1_0.pddl", "delivery:instance_2_2_0.pddl", "gripper:p-1-0.pddl", "gripper:p-2-0.pddl", "miconic:p-2-2-0.pddl", "miconic:p-3-3-0.pddl", "reward", "visitall"]
    TIME_LIMIT = 180
ATTRIBUTES = [
    #Attribute("generate_time_complexity_5", absolute=True, min_wins=True, scale="linear"),
    #Attribute("generate_memory_complexity_5", absolute=True, min_wins=True, scale="linear"),
    #Attribute("num_generated_features_complexity_5", absolute=True, min_wins=True, scale="linear"),
    #Attribute("num_novel_features_complexity_5", absolute=True, min_wins=True, scale="linear"),
    Attribute("generate_time_complexity_10", absolute=True, min_wins=True, scale="linear"),
    Attribute("generate_memory_complexity_10", absolute=True, min_wins=True, scale="linear"),
    Attribute("num_generated_features_complexity_10", absolute=True, min_wins=True, scale="linear"),
    Attribute("num_novel_features_complexity_10", absolute=True, min_wins=True, scale="linear"),
    Attribute("num_states", absolute=True, min_wins=False, scale="linear"),
    Attribute("num_dynamic_atoms", absolute=True, min_wins=False, scale="linear"),
    Attribute("num_static_atoms", absolute=True, min_wins=False, scale="linear"),
    Attribute("evaluate_time", absolute=True, min_wins=True, scale="linear"),
]
MEMORY_LIMIT = (16 * 3000) * 0.98

GENERATOR_TIME_LIMIT = 2 * 3600
GENERATOR_FEATURE_LIMIT = 1000000

# Create a new experiment.
exp = Experiment(environment=ENV)
# Add custom parser for FF.
exp.add_parser("experiment_parser.py")

for task in suites.build_suite(BENCHMARKS_DIR, SUITE):
    for num_threads in [1,2,4,8,12,16]:
        for complexity in [10]:
            run = exp.add_run()
            # Create symbolic links and aliases. This is optional. We
            # could also use absolute paths in add_command().
            run.add_resource("domain", task.domain_file, symlink=True)
            run.add_resource("problem", task.problem_file, symlink=True)
            run.add_resource("main", "main.py", symlink=True)
            # 'ff' binary has to be on the PATH.
            # We could also use exp.add_resource().
            run.add_command(
                f"complexity-{complexity}-{num_threads}",
                ["python3", "main.py", "--domain", "{domain}", "--instance", "{problem}", "--c", complexity, "--t", GENERATOR_TIME_LIMIT, "--f", GENERATOR_FEATURE_LIMIT, "--n", num_threads],
                time_limit=num_threads * TIME_LIMIT,
                memory_limit=MEMORY_LIMIT,
            )
            # AbsoluteReport needs the following properties:
            # 'domain', 'problem', 'algorithm', 'coverage'.
            run.set_property("domain", task.domain)
            run.set_property("problem", task.problem)
            run.set_property("algorithm", f"complexity-{complexity}-{num_threads}")
            # BaseReport needs the following properties:
            # 'time_limit', 'memory_limit'.
            run.set_property("time_limit", TIME_LIMIT)
            run.set_property("memory_limit", MEMORY_LIMIT)
            # Every run has to have a unique id in the form of a list.
            # The algorithm name is only really needed when there are
            # multiple algorithms.
            run.set_property("id", [f"complexity-{complexity}-{num_threads}", task.domain, task.problem])


def fetch_algorithm(exp, expname, algo, *, new_algo=None):
    """Fetch (and possibly rename) a single algorithm from *expname*."""
    new_algo = new_algo or algo

    def rename_and_filter(run):
        if run["algorithm"] == algo:
            run["algorithm"] = new_algo
            run["id"][0] = new_algo
            return run
        return False

    exp.add_fetcher(
        f"data/{expname}-eval",
        filter=rename_and_filter,
        name=f"fetch-{new_algo}-from-{expname}",
        merge=True,
    )


# Add step that writes experiment files to disk.
exp.add_step("build", exp.build)

# Add step that executes all runs.
exp.add_step("start", exp.start_runs)

# Add step that collects properties from run directories and
# writes them to *-eval/properties.
exp.add_fetcher(name="fetch")

fetch_algorithm(exp, "0_drexler-et-al-kr2021-IPC-init", "siwr-1", new_algo="siwr-1-init")
fetch_algorithm(exp, "0_drexler-et-al-kr2021-IPC-init", "siwr-2", new_algo="siwr-2-init")

fetch_algorithm(exp, "1_drexler-et-al-kr2021-IPC-pimpl", "siwr-1", new_algo="siwr-1-pimpl")
fetch_algorithm(exp, "1_drexler-et-al-kr2021-IPC-pimpl", "siwr-2", new_algo="siwr-2-pimpl")

fetch_algorithm(exp, "2_drexler-et-al-kr2021-IPC-state", "siwr-1", new_algo="siwr-1-state")
fetch_algorithm(exp, "2_drexler-et-al-kr2021-IPC-state", "siwr-2", new_algo="siwr-2-state")

# Make a report.
exp.add_report(BaseReport(attributes=ATTRIBUTES), outfile="report.html")

# Parse the commandline and run the specified steps.
exp.run_steps()