#!/usr/bin/env python3

import argparse

from pathlib import Path

from learner.learner import learn_sketch_for_problem_class
from learner.src.asp.encoding_type import EncodingType


def encoding_type(value):
    try:
        return EncodingType[value]
    except KeyError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid encoding type.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sketch learner.")
    parser.add_argument("--domain_filepath", type=Path, required=True, help="The path to the domain file.")
    parser.add_argument("--problems_directory", type=Path, required=True, help="The directory containing the problem files.")
    parser.add_argument("--workspace", type=Path, required=True, help="The directory containing intermediate files.")
    parser.add_argument("--width", type=int, default=1, help="The upper bound on the sketch width.")
    parser.add_argument("--closed_Q", action='store_true', default=True, help="Whether the search space is closed. Default is True.")
    parser.add_argument("--max_num_states_per_instance", type=int, default=1000, help="The maximum number of states per instance.")
    parser.add_argument("--max_time_per_instance", type=int, default=10, help="The maximum time (in seconds) per instance.")
    parser.add_argument("--encoding_type", type=encoding_type, default=EncodingType.D2, choices=["d2", "explicit"], help="The encoding type for the sketch learner.")
    parser.add_argument("--max_num_rules", type=int, default=4, help="The maximum number of rules used in the explicit encoding.")
    parser.add_argument("--enable_goal_separating_features", action='store_true', default=False, help="Whether to enable goal separating features. Default is True.")
    parser.add_argument("--disable_feature_generation", action='store_true', default=True, help="Whether to enable feature generation. Default is True.")
    parser.add_argument("--concept_complexity_limit", type=int, default=9, help="The complexity limit for concepts.")
    parser.add_argument("--role_complexity_limit", type=int, default=9, help="The complexity limit for roles.")
    parser.add_argument("--boolean_complexity_limit", type=int, default=9, help="The complexity limit for boolean features.")
    parser.add_argument("--count_numerical_complexity_limit", type=int, default=9, help="The complexity limit for count numerical features.")
    parser.add_argument("--distance_numerical_complexity_limit", type=int, default=9, help="The complexity limit for distance numerical features.")
    parser.add_argument("--feature_limit", type=int, default=1000000, help="The limit for the number of features.")
    parser.add_argument("--additional_booleans", nargs='*', default=None, help="Additional boolean features to include.")
    parser.add_argument("--additional_numericals", nargs='*', default=None, help="Additional numerical features to include.")

    args = parser.parse_args()

    learn_sketch_for_problem_class(args.domain_filepath.resolve(),
                                   args.problems_directory.resolve(),
                                   args.workspace.resolve(),
                                   args.width,
                                   args.closed_Q,
                                   args.max_num_states_per_instance,
                                   args.max_time_per_instance,
                                   args.encoding_type,
                                   args.max_num_rules,
                                   args.enable_goal_separating_features,
                                   args.disable_feature_generation,
                                   args.concept_complexity_limit,
                                   args.role_complexity_limit,
                                   args.boolean_complexity_limit,
                                   args.count_numerical_complexity_limit,
                                   args.distance_numerical_complexity_limit,
                                   args.feature_limit,
                                   args.additional_booleans,
                                   args.additional_numericals)
