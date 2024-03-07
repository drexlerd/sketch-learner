#! /usr/bin/env python3

"""
Example experiment for running Singularity planner images.

Note that Downward Lab assumes that the evaluated algorithms are written
in good faith. It is not equipped to handle malicious code. For example,
it would be easy to write planner code that bypasses the time and memory
limits set within Downward Lab. If you're running untrusted code, we
recommend using cgroups to enforce resource limits.

A note on running Singularity on clusters: reading large Singularity
files over the network is not optimal, so we recommend copying the
images to a local filesystem (e.g., /tmp/) before running experiments.
"""

import os
from pathlib import Path

from downward import suites
from downward.reports.absolute import AbsoluteReport
from lab.experiment import Experiment
from lab.reports import Attribute, arithmetic_mean
from lab.parser import Parser

import project


def coverage(content, props):
    props["coverage"] = int("cost" in props and "valid_plan_value" in props)


def error(content, props):
    if props.get("planner_exit_code") == 0:
        props["error"] = "none"


class LapktSIWRSingularityParser(Parser):
    def __init__(self):
        super().__init__()
        self.add_pattern(
            "node", r"node: (.+)\n", type=str, file="driver.log", required=True
        )
        self.add_pattern("cost", r"Plan found with cost: (\d+)\n", type=int)
        self.add_pattern("expanded", r"Expanded (\d+)\n", type=int)
        self.add_pattern("generated", r"Generated (\d+)\n", type=int)
        self.add_pattern("total_time", r"Time: (.+)\n", type=float)
        self.add_pattern("valid_plan_value", r"Final value: (\d+) \n", type=int)
        self.add_pattern("maximum_effective_width", r"Max ef. width: (\d+)\n", type=int)
        self.add_pattern("average_effective_width", r"Average ef. width: (.+)\n", type=float)
        self.add_function(coverage)


# Create custom report class with suitable info and error attributes.
class BaseReport(AbsoluteReport):
    INFO_ATTRIBUTES = []
    ERROR_ATTRIBUTES = [
        "domain",
        "problem",
        "algorithm",
        "unexplained_errors",
        "error",
        "node",
    ]


ATTRIBUTES = [
    "run_dir",
    "length",
    "cost",
    Attribute(name="coverage", absolute=True, min_wins=False),
    Attribute(name="valid_plan_value", absolute=True, min_wins=False),
    "error",
    "expanded",
    "generated",
    Attribute("maximum_effective_width", function=max),
    Attribute("average_effective_width", function=arithmetic_mean),
    Attribute("total_time_feature_evaluation", function=sum),
    Attribute(name="total_time", absolute=True, function=max),
]


DIR = Path(__file__).resolve().parent
BENCHMARKS_DIR = DIR.parent.parent / "testing"/ "benchmarks"
print("Benchmark directory:", BENCHMARKS_DIR)
if project.REMOTE:
    SUITE = ["blocks_4_clear", "blocks_4_on", "delivery", "gripper", "miconic", "reward", "spanner", "visitall"]
    ENV = project.TetralithEnvironment(
        email="dominik.drexler@liu.se",
        extra_options="#SBATCH --account=naiss2023-5-314",
        memory_per_cpu="8G")
else:
    SUITE = ["blocks_4_clear:p-51-0.pddl", "blocks_4_on:p-51-0.pddl", "childsnack:p01.pddl", "delivery:instance_3_2_0.pddl", "gripper:p01.pddl", "miconic:p01.pddl", "reward:instance_5x5_0.pddl", "spanner:pfile01-001.pddl", "visitall:p01.pddl"]
    ENV = project.LocalEnvironment(processes=4)
SKETCHES_DIR = DIR.parent.parent / "learning" / "workspace-sym-2024-3-7"
print("Sketches directory:", SKETCHES_DIR)

exp = Experiment(environment=ENV)
exp.add_parser(LapktSIWRSingularityParser())

IMAGES_DIR = DIR.parent.parent / "testing" / "planners"
print(IMAGES_DIR)

def get_image(name):
    planner = name.replace("-", "_")
    image = os.path.join(IMAGES_DIR, name + ".sif")
    assert os.path.exists(image), image
    return planner, image


IMAGES = [get_image("siwr")]

for planner, image in IMAGES:
    exp.add_resource(planner, image, symlink=True)

singularity_script = os.path.join(DIR, "run-singularity-siwr.sh")
exp.add_resource("run_singularity", singularity_script)

TIME_LIMIT = 1800
MEMORY_LIMIT = 8000
for planner, _ in IMAGES:
    for task in suites.build_suite(BENCHMARKS_DIR, SUITE):
        for w in range(0,3):
            sketch_filename = SKETCHES_DIR / f"{task.domain}_{w}" / "output" / f"sketch_minimized_{w}.txt"
            if not sketch_filename.is_file():
                continue
            run = exp.add_run()
            run.add_resource("domain", task.domain_file, "domain.pddl")
            run.add_resource("problem", task.problem_file, "problem.pddl")
            run.add_resource("sketch", sketch_filename)
            run.add_command(
                "run-planner",
                [
                    "{run_singularity}",
                    f"{{{planner}}}",
                    "{domain}",
                    "{problem}",
                    "{sketch}",
                    w,
                    "plan.ipc",
                ],
                time_limit=TIME_LIMIT,
                memory_limit=MEMORY_LIMIT,
            )
            run.set_property("domain", task.domain)
            run.set_property("problem", task.problem)
            run.set_property("algorithm", f"{planner}_{w}")
            run.set_property("id", [f"{planner}_{w}", task.domain, task.problem])

# Add step that writes experiment files to disk.
exp.add_step("build", exp.build)

# Add step that executes all runs.
exp.add_step("start", exp.start_runs)

exp.add_step("parse", exp.parse)

# Add step that collects properties from run directories and
# writes them to *-eval/properties.
exp.add_fetcher(name="fetch")

# Make a report.
report = os.path.join(exp.eval_dir, f"{exp.name}.html")
exp.add_report(BaseReport(attributes=ATTRIBUTES), outfile=report)

# Parse the commandline and run the specified steps.
exp.run_steps()
