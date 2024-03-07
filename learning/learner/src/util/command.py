import os

from contextlib import contextmanager


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


@contextmanager
def change_dir(destination, enable=True):
    # Save the current directory before entering the try block
    original_directory = os.getcwd()
    try:
        if enable:
            # Create directory if it does not exist
            os.makedirs(destination, exist_ok=True)
            # Change to the new directory
            os.chdir(destination)
            # Yield control back to the with block
        yield
    finally:
        # No matter what happens, change back to the original directory
        os.chdir(original_directory)
