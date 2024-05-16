import logging
import sys

from . import constants as CONST
from .loggerformat import LoggerFormat

def get_logger(name: str, level=logging.INFO,
               date_width: int=CONST.ASCTIME_WIDTH,
               module_width: int=CONST.ASCTIME_WIDTH,
               func_width: int=CONST.FUNC_WIDTH,
               level_width: int=CONST.LEVEL_WIDTH,
               custom_format: str=None,
               logger_format: LoggerFormat=None,
               dateformat=CONST.DATE_FORMAT,
               ):
    if custom_format:
        line_format = custom_format
    elif logger_format:
        line_format = str(logger_format)
    else:
        line_format = f"%(asctime)s | " if date_width else ""
        line_format +=f"%(module){module_width}s.py | " if module_width else ""
        line_format +=f"%(funcName){func_width}s() | " if func_width else ""
        line_format +=f"%(levelname)-{level_width}s | " if level_width else ""
        line_format +=f"%(message)s"
        
    date_format = dateformat

    logging.basicConfig(level=level, format=line_format, datefmt=date_format)
    logger = logging.getLogger(name)
    return logger


if __name__ == '__main__':
    # logger = get_logger( 'test', date_width=0, func_width=0, module_width=0 )
    from .loggerformat import default_config
    print(f'{default_config =!s}')
    logger = get_logger('test', logger_format=default_config)
    logger.info('testing the logger!')