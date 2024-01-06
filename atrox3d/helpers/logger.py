import logging
import sys

class CONST:
    pass

CONST.DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
CONST.ASCTIME_WIDTH = len(CONST.DATE_FORMAT)
CONST.MODULENAME_WIDTH = 12
CONST.FUNCNAME_WIDTH = 12
CONST.LEVELNAME_WIDTH = str(len("CRITICAL"))

def get_logger(name: str, level=logging.INFO,
               date_width=CONST.ASCTIME_WIDTH,
               module_width=CONST.ASCTIME_WIDTH,
               func_width=CONST.FUNCNAME_WIDTH,
               level_width=CONST.LEVELNAME_WIDTH,
               custom_format=None,
               dateformat=CONST.DATE_FORMAT,
               ):
    if custom_format:
        line_format = custom_format
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
    logger = get_logger( 'test', date_width=0, func_width=0, module_width=0 )
    logger.info('testing')