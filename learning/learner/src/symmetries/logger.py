import logging
import sys

from datetime import datetime


formatter = logging.Formatter('%(asctime)s - %(message)s')


def initialize_logger(name: str):
    return logging.getLogger(name)


def add_console_handler(logger: logging.Logger):
    global formatter
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return handler


def add_file_handler(logger: logging.Logger, name: str):
    global formatter
    formatted_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    handler = logging.FileHandler(f"log/{formatted_datetime}_{name}.log", mode="w")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return handler


def remove_console_handler(logger: logging.Logger, console_handler: logging.StreamHandler):
    logger.removeHandler(console_handler)


def remove_file_handler(logger: logging.Logger, file_handler: logging.FileHandler):
    file_handler.close()
    logger.removeHandler(file_handler)
