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
        try_delete(props, "generated")
        try_delete(props, "expanded")
        try_delete(props, "pruned")
        try_delete(props, "width_average")
        try_delete(props, "width_maximum")


def error(content, props):
    if props.get("planner_exit_code") == 0:
        props["error"] = "none"
    elif "CPU time limit exceeded" in content:
        props["error"] = "timeout"
    elif ";; NOT I-REACHABLE ;;" in content:
        props["error"] = "none"
    else:
        props["error"] = "some-error-occured"


def not_i_reachable(content, props):
    if ";; NOT I-REACHABLE ;;" in content:
        props["not_i_reachable"] = 1
    else:
        props["not_i_reachable"] = 0


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
    parser.add_pattern("generated", r"Nodes generated during search: (\d+)\n", type=int)
    parser.add_pattern("expanded", r"Nodes expanded during search: (\d+)\n", type=int)
    parser.add_pattern("pruned", r"Nodes pruned by bound: (\d+)\n", type=int)
    parser.add_pattern("width_average", r"Average ef. width: (.+)\n", type=float)
    parser.add_pattern("width_maximum", r"Max ef. width: (\d+)\n", type=int)
    parser.add_function(coverage)
    parser.add_function(error)
    parser.add_function(not_i_reachable)
    parser.parse()

if __name__ == "__main__":
    main()
