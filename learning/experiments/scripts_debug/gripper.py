import argparse
import os
import subprocess

from pathlib import Path

SKETCH_LEARNER_DIR = Path(os.getenv("SKETCH_LEARNER_DIR"))


def run(domain_filepath: Path, problems_directory: Path, workspace: Path, width: int):
    additional_booleans = [
        "b_empty(c_and(c_primitive(at-robby,0),c_one_of(rooma)))",  # robot at room b
        "b_empty(r_diff(r_primitive(at_g,0,1), r_primitive(at,0,1)))"  # goal separating feature
    ]
    additional_numericals = [
        "n_count(r_primitive(carry,0,1))",  # 4 num balls that the robot carries
        "n_count(r_diff(r_primitive(at_g,0,1), r_primitive(at,0,1)))",  # 4 num misplaced balls, i.e., num balls at roomb
    ]

    subprocess.call([
        "python3", SKETCH_LEARNER_DIR / "learning" / "main.py",
        "--domain_filepath", str(domain_filepath),
        "--problems_directory", str(problems_directory),
        "--workspace", str(workspace),
        "--width", str(width),
        "--disable_feature_generation"]
        + ["--additional_booleans", ] + additional_booleans
        + ["--additional_numericals",] + additional_numericals
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gripper debug experiment.")
    parser.add_argument("--domain_filepath", type=Path, required=True, help="The path to the domain file.")
    parser.add_argument("--problems_directory", type=Path, required=True, help="The directory containing the problem files.")
    parser.add_argument("--workspace", type=Path, required=True, help="The directory containing intermediate files.")
    parser.add_argument("--width", type=int, default=1, help="The upper bound on the sketch width.")

    args = parser.parse_args()

    run(args.domain_filepath, args.problems_directory, args.workspace, args.width)