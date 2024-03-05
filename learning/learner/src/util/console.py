import logging
import sys

formatter = logging.Formatter('%(asctime)s - %(message)s')


def add_console_handler(logger: logging.Logger, level):
    global formatter
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    return handler


def print_separation_line():
    print("=" * 80)
