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


def error(content, props):
    if props.get("planner_exit_code") == 0:
        props["error"] = "none"


def main():
    parser = Parser()
    parser.add_pattern(
        "node", r"node: (.+)\n", type=str, file="driver.log", required=True
    )
    parser.add_pattern("length", r".+ Plan length: (\d+) step\(s\).\n", type=int)
    parser.add_pattern("cost", r".+ Plan cost: (\d+)\n", type=int)
    parser.add_pattern("expanded", r".+ Expanded (\d+) state\(s\).\n", type=int)
    parser.add_pattern("generated", r".+ Generated (\d+) state\(s\).\n", type=int)
    parser.add_pattern("total_time", r".+ Total time: (.+)s\n", type=float)
    parser.parse()

if __name__ == "__main__":
    main()
