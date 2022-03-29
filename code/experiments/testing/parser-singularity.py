#! /usr/bin/env python

import re

from lab.parser import Parser


def try_delete(map, key):
    try:
        del map[key]
    except KeyError:
        pass


def coverage(content, props):
    props["coverage"] = int("cost" in props)
    if not props["coverage"]:
        try_delete(props, "total_time")
        try_delete(props, "cost")


def error(content, props):
    if props.get("planner_exit_code") == 0:
        props["error"] = "none"
    else:
        props["error"] = "some-error-occured"


def main():
    parser = Parser()
    parser.add_pattern(
        "planner_exit_code",
        r"run-planner exit code: (.+)\n",
        type=int,
        file="driver.log",
        required=True,
    )
    parser.add_pattern(
        "node", r"node: (.+)\n", type=str, file="driver.log", required=True
    )
    parser.add_pattern(
        "planner_wall_clock_time",
        r"run-planner wall-clock time: (.+)s",
        type=float,
        file="driver.log",
        required=True,
    )
    parser.add_pattern("total_time", r"Singularity runtime: (.+?)s", type=float)
    parser.add_pattern("cost", r"\nFinal value: (.+)\n", type=int)
    parser.add_function(coverage)
    parser.add_function(error)
    parser.parse()

if __name__ == "__main__":
    main()
