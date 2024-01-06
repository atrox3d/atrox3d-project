import logging
import sys

class CONST:
    pass

CONST.DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
CONST.ASCTIME_WIDTH = len(CONST.DATE_FORMAT)
CONST.MODULENAME_WIDTH = 12
CONST.FUNCNAME_WIDTH = 12
CONST.LEVELNAME_WIDTH = str(len("CRITICAL"))
# CONST.LINE_FORMAT = (
#             f"%(asctime)s | "
#             f"%(module){CONST.MODULENAME_WIDTH}s.py | "
#             f"%(funcName){CONST.FUNCNAME_WIDTH}s() | "
#             f"%(levelname)-{CONST.LEVELNAME_WIDTH}s | "
#             f"%(message)s"
#     )


def get_logger(name: str, level=logging.INFO,
               asctime_width=CONST.ASCTIME_WIDTH,
               modulename_width=CONST.ASCTIME_WIDTH,
               funcname_width=CONST.FUNCNAME_WIDTH,
               levelname_width=CONST.LEVELNAME_WIDTH,
               lineformat=None,
               dateformat=CONST.DATE_FORMAT,
               ):
    print(f'{lineformat=}')
    print(f'{asctime_width=}')
    print(f'{modulename_width=}')
    print(f'{funcname_width=}')
    print(f'{levelname_width=}')

    if lineformat:
        line_format = lineformat
    else:
        line_format = f"%(asctime)s | " if asctime_width else ""
        line_format +=f"%(module){modulename_width}s.py | " if modulename_width else ""
        line_format +=f"%(funcName){funcname_width}s() | " if funcname_width else ""
        line_format +=f"%(levelname)-{levelname_width}s | " if levelname_width else ""
        line_format +=f"%(message)s"
    
    print(f'{line_format=}')
    date_format = dateformat or CONST.DATE_FORMAT

    logging.basicConfig(
        level=level,
        format=line_format,
        datefmt=date_format,
        # stream=sys.stdout
    )
    logger = logging.getLogger(name)
    return logger


if __name__ == '__main__':
    logger = get_logger(
                    'test',
                    asctime_width=0, 
                    funcname_width=0,
                    modulename_width=0
                )

    logger.info('testing')