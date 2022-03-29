#! /usr/bin/env python

from pathlib import Path
import shutil
import subprocess

from downward import suites
from downward.reports.absolute import AbsoluteReport
from downward.experiment import FastDownwardExperiment
from lab.experiment import Experiment, Run
from lab import tools
from lab.reports import Attribute, arithmetic_mean

import project

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


DIR = Path(__file__).resolve().parent
SIWR_PATH = DIR.parent / "siwr.py"
BENCHMARKS_DIR = DIR / "benchmarks" / "downward-benchmarks"
SKETCHES_DIR = DIR / "sketches" / "handcrafted"
if project.REMOTE:
    SUITE = ["barman", "childsnack", "driverlog", "floortile", "grid", "schedule", "tpp"]
    ENV = project.TetralithEnvironment(
        email="dominik.drexler@liu.se",
        extra_options="#SBATCH --account=snic2021-5-330",
        memory_per_cpu="3G")
else:
    SUITE = ["barman:p1-11-4-15.pddl", "childsnack:child-snack_pfile05.pddl", "driverlog:p01.pddl", "floortile:p01-4-3-2.pddl", "grid:prob01.pddl", "schedule:probschedule-2-0.pddl", "tpp:p01.pddl"]
    ENV = project.LocalEnvironment(processes=2)


ATTRIBUTES = [
    "cost",
    "coverage",
    "nodes_generated",
    "nodes_expanded",
    "nodes_pruned",
    "width_average",
    "width_maximum",
    "total_time",
    "not_i_reachable"
]

TIME_LIMIT = 1800
MEMORY_LIMIT = 3000

exp = Experiment(environment=ENV)
exp.add_parser("experiment_parser.py")

for task in suites.build_suite(BENCHMARKS_DIR, SUITE):
    for w in range(3):
        sketch_name = f"{task.domain}_{w}.txt"
        sketch_filename = SKETCHES_DIR / task.domain / sketch_name
        # if no sketch exists for this width we skip
        if not sketch_filename.is_file(): continue

        run = exp.add_run()

        run.add_resource("domain", task.domain_file, symlink=True)
        run.add_resource("problem", task.problem_file, symlink=True)
        run.add_resource("sketch", sketch_filename, symlink=True)
        # 'ff' binary has to be on the PATH.
        # We could also use exp.add_resource().
        run.add_resource("planner", SIWR_PATH, symlink=True)
        run.add_command(
            "run-planner",
            ["python3", "{planner}",  "{domain}", "{problem}", "{sketch}", "plan.txt"],
            time_limit=TIME_LIMIT,
            memory_limit=MEMORY_LIMIT,
        )
        # AbsoluteReport needs the following properties:
        # 'domain', 'problem', 'algorithm', 'coverage'.
        run.set_property("domain", task.domain)
        run.set_property("problem", task.problem)
        run.set_property("algorithm", f"siwr-{w}")
        # BaseReport needs the following properties:
        # 'time_limit', 'memory_limit'.
        run.set_property("time_limit", TIME_LIMIT)
        run.set_property("memory_limit", MEMORY_LIMIT)
        # Every run has to have a unique id in the form of a list.
        # The algorithm name is only really needed when there are
        # multiple algorithms.
        run.set_property("id", [f"siwr-{w}", task.domain, task.problem])


# Add step that writes experiment files to disk.
exp.add_step("build", exp.build)

# Add step that executes all runs.
exp.add_step("start", exp.start_runs)

# Add step that collects properties from run directories and
# writes them to *-eval/properties.
exp.add_fetcher(name="fetch")

# Make a report.
exp.add_report(BaseReport(attributes=ATTRIBUTES), outfile="report.html")

# Parse the commandline and run the specified steps.
exp.run_steps()
