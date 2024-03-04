import os


def read_file(filename):
    """ Read a file, line by line, ignoring end-of-line characters"""
    with open(filename, "r") as f:
        for line in f:
            yield line.rstrip('\n')


def write_file(filename, content):
    """ """
    with open(filename, "w") as f:
        f.write(content)


def change_working_directory(path):
    print("Changing working directory: ", path)
    os.chdir(path)


def create_experiment_workspace(dirname):
    os.makedirs(dirname, exist_ok=True)
