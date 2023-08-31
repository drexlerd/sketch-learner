import logging
import pickle


def serialize(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)


def deserialize(filename):
    with open(filename, 'rb') as f:
        try:
            data = pickle.load(f)
        except EOFError as e:
            logging.error("Deserialization error: couldn't unpicle file '{}'".format(filename))
            raise
    return data
