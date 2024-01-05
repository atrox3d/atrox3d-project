import logging
import sys


def get_logger(name, level=logging.INFO):
    """
    get standard logger to stdout, level INFO
    :param name:
    :param level:
    :return:
    """
    modulename_width = 12
    funcname_width = 12
    levelname_width = str(len("CRITICAL"))

    line_format = (
            f"%(asctime)s | "
            f"%(module){modulename_width}s.py | "
            # f"%(funcName){funcname_width}s() | "
            f"%(levelname)-{levelname_width}s | "
            f"%(message)s"
    )
    date_format = '%Y/%m/%d %H:%M:%S'

    logging.basicConfig(
        level=level,
        format=line_format,
        datefmt=date_format,
        # stream=sys.stdout
    )
    logger = logging.getLogger(name)
    return logger
