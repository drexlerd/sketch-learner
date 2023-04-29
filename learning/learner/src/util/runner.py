import importlib
import os
import sys

from pathlib import Path

from learner.src.util.bootstrap import setup_argparser
from learner.src.util.defaults import generate_experiment


def import_from_file(filename):
    """ Import a module from a given file path """
    import importlib.util
    spec = importlib.util.spec_from_file_location("imported", filename)
    if spec is None:
        report_and_exit(f'Could not import Python module "{filename}"')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def import_experiment_file(filename):
    """ Import a module from a given file path """
    if os.path.isfile(filename):
        return import_from_file(filename)
    try:
        return importlib.import_module(filename)
    except ImportError:
        report_and_exit(f'No script named "{filename}.py" found on current directory')


def report_and_exit(msg):
    print(f"ERROR: {msg}")
    sys.exit(-1)


def do(domain_filename, task_dir, workspace, expid=None, pipeline=None, width=None, concept_complexity_limit=None, role_complexity_limit=None, boolean_complexity_limit=None, count_numerical_complexity_limit=None, distance_numerical_complexity_limit=None):
    experiment = dict()
    if expid is not None:
        name_parts = expid.split(":")
        if len(name_parts) != 2:
            report_and_exit(f'Wrong experiment ID syntax "{expid}". Expected format <domain>:<experiment_name>')

        scriptname, expname = name_parts
        mod = import_experiment_file(scriptname)

        try:
            experiments = mod.experiments()
        except AttributeError:
            report_and_exit(f'Expected method "experiments" not found in script "{scriptname}"')

        if expname not in experiments:
            report_and_exit(f'No experiment named "{expname}" in current experiment script')
        experiment = experiments[expname]

        assert "domain_filename" in experiment
        assert "instance_filenames" in experiment
    else:
        experiment["domain_filename"] = domain_filename
        experiment["instance_filenames"] = list(task_dir.iterdir())
    parameters = experiment

    # overwrite parameters given as arguments in the root call
    parameters["workspace"] = workspace
    parameters["pipeline"] = pipeline
    if width is not None:
        parameters["width"] = width
    if concept_complexity_limit is not None:
        parameters["concept_complexity_limit"] = concept_complexity_limit
    if role_complexity_limit is not None:
        parameters["role_complexity_limit"] = role_complexity_limit
    if boolean_complexity_limit is not None:
        parameters["boolean_complexity_limit"] = boolean_complexity_limit
    if count_numerical_complexity_limit is not None:
        parameters["count_numerical_complexity_limit"] = count_numerical_complexity_limit
    if distance_numerical_complexity_limit is not None:
        parameters["distance_numerical_complexity_limit"] = distance_numerical_complexity_limit

    # Sets up experiment
    experiment = generate_experiment(**parameters)

    experiment.run()


def run():
    args = setup_argparser().parse_args(sys.argv[1:])
    do( Path(args.domain).resolve(),
        Path(args.task_dir).resolve(),
        Path(args.workspace).resolve(),
        args.exp_id,
        args.pipeline,
        args.width,
        args.concept_complexity_limit,
        args.role_complexity_limit,
        args.boolean_complexity_limit,
        args.count_numerical_complexity_limit,
        args.distance_numerical_complexity_limit)
