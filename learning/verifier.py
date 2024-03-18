#!/usr/bin/env python3

import argparse

from pathlib import Path

from learner.verifier import verify_sketch_for_problem_class
from learner.src.asp.encoding_type import EncodingType


def encoding_type(value):
    try:
        return EncodingType[value]
    except KeyError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid encoding type.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sketch verifier.")
    parser.add_argument("--domain_filepath", type=Path, required=True, help="The path to the domain file.")
    parser.add_argument("--problem_filepath", type=Path, required=True, help="The directory containing the problem files.")
    parser.add_argument("--sketch_filepath", type=Path, required=True, help="The path to the sketch file.")
    parser.add_argument("--workspace", type=Path, required=True, help="The directory containing intermediate files.")
    parser.add_argument("--width", type=int, default=1, help="The upper bound on the sketch width.")
    parser.add_argument("--disable_closed_Q", action='store_true', default=False, help="Whether the search space is closed. Default is True.")
    parser.add_argument("--max_num_states_per_instance", type=int, default=10000, help="The maximum number of states per instance.")
    parser.add_argument("--max_time_per_instance", type=int, default=10, help="The maximum time (in seconds) per instance.")
    parser.add_argument("--enable_goal_separating_features", action='store_true', default=False, help="Whether to enable goal separating features. Default is True.")
    parser.add_argument("--enable_dump_files", action='store_true', default=False, help="Whether data should be written to files.")


    args = parser.parse_args()

    verify_sketch_for_problem_class(args.domain_filepath.resolve(),
                                   args.problem_filepath.resolve(),
                                   args.sketch_filepath.resolve(),
                                   args.workspace.resolve(),
                                   args.width,
                                   args.disable_closed_Q,
                                   args.max_num_states_per_instance,
                                   args.max_time_per_instance,
                                   args.enable_goal_separating_features,
                                   args.enable_dump_files)
