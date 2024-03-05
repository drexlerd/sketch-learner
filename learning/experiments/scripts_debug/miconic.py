
import argparse
import subprocess

from pathlib import Path


def run(domain_filepath: Path, problems_directory: Path, workspace: Path, width: int):
    additional_booleans=[
        "b_empty(c_and(c_not(c_primitive(served,0)),c_primitive(served_g,0)))",  # goal separating feature
    ]
    additional_numericals=[
        "n_count(c_primitive(served,0))",
        "n_count(c_primitive(boarded,0))",
        "n_count(c_and(c_primitive(boarded,0),c_some(r_primitive(destin,0,1),c_primitive(lift-at,0))))",
        "n_count(c_some(r_primitive(origin,0,1),c_primitive(lift-at,0)))",
    ]

    subprocess.call([
        "python3", "../../main.py",
        "--domain_filepath", str(domain_filepath),
        "--problems_directory", str(problems_directory),
        "--workspace", str(workspace),
        "--width", str(width),
        "--disable_feature_generation"]
        + ["--additional_booleans", ] + additional_booleans
        + ["--additional_numericals",] + additional_numericals
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Miconic debug experiment.")
    parser.add_argument("--domain_filepath", type=Path, required=True, help="The path to the domain file.")
    parser.add_argument("--problems_directory", type=Path, required=True, help="The directory containing the problem files.")
    parser.add_argument("--workspace", type=Path, required=True, help="The directory containing intermediate files.")
    parser.add_argument("--width", type=int, default=1, help="The upper bound on the sketch width.")

    args = parser.parse_args()

    run(args.domain_filepath, args.problems_directory, args.workspace, args.width)