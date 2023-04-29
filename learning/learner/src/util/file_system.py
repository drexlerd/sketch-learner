import os
import errno
import jsonpickle


def create_directory_for_filename(filename):
    """ Creates all directories necessary to store the given filename. """
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def write_object_to_file(filename, object):
    """ Writes json content to the given file. """
    create_directory_for_filename(filename)
    with open(filename, "w") as f:
        f.write(jsonpickle.encode(object, keys=True))


def read_object_from_file(filename):
    with open(filename, "r") as f:
        return jsonpickle.decode(f.readline(), keys=True)

