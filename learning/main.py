#!/usr/bin/env python3

import argparse

from pathlib import Path

from learner.learner import learn_sketch_for_problem_class


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sketch learner.")
    parser.add_argument("--domain_filepath", type=str, required=True, help="The path to the domain file.")
    parser.add_argument("--problems_directory", type=str, required=True, help="The directory containing the problem files.")
    parser.add_argument("--workspace", type=str, required=True, help="The directory containing intermediate files.")
    parser.add_argument("--width", type=int, default=1, help="The upper bound on the sketch width.")

    args = parser.parse_args()

    learn_sketch_for_problem_class(Path(args.domain_filepath).resolve(),
                                   Path(args.problems_directory).resolve(),
                                   Path(args.workspace).resolve(),
                                   args.width)
