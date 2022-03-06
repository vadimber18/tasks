import logging
import os
from logging.handlers import TimedRotatingFileHandler

FORMATTER = "%(asctime)s.%(msecs)03dZ [%(name)s] %(levelname)s: %(message)s"
DATEFMT = "%Y-%m-%dT%H:%M:%S"

format_ = logging.Formatter(FORMATTER, DATEFMT)


SERVICE = os.getenv("SERVICE", "tasks-consumer")


def get_console_handler(format_=format_):
    console_handler = logging.StreamHandler(os.sys.stdout)
    console_handler.setFormatter(format_)
    return console_handler


def get_file_handler(format_=format_):
    file_handler = TimedRotatingFileHandler(
        filename=f"/var/log/{SERVICE}.log",
        interval=1,  # log files per day
        when="midnight",
        backupCount=31,
    )  # per month
    file_handler.setFormatter(format_)
    return file_handler


def get_logger():
    logg = logging.getLogger(SERVICE)
    logg.setLevel(logging.DEBUG)
    logg.addHandler(get_console_handler())
    logg.addHandler(get_file_handler())
    logg.propagate = False
    return logg
