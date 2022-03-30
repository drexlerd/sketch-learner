import os
from .file_system import create_directory_for_filename


def filename_core(filename):
    return os.path.splitext(os.path.basename(filename))[0]


def compute_filename(experiment_dir, instance, filename):
    result = os.path.join(experiment_dir, filename_core(instance), filename)
    create_directory_for_filename(result)
    return result


def compute_filenames(experiment_dir, instances, filename):
    return [compute_filename(experiment_dir, instance, filename) for instance in instances]


def compute_serialization_name(basedir, name):
    return os.path.join(basedir, f'{name}.pickle')


def compute_info_filename(config, name):
    return os.path.join(config["experiment_dir"], name)
