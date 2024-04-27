import logging
from pathlib import Path

print('testmain: define loggger')
LOGFILE = str(Path(__file__).parent / Path(__file__).stem) + '.log'
handlers = [
    logging.FileHandler(LOGFILE, mode='w'),
    logging.StreamHandler()
]
logging.basicConfig(level='DEBUG', format='%(levelname)5s | %(message)s', handlers=handlers)

logger = logging.getLogger(__name__)
logger.debug(f"import {__name__}")

from atrox3d.simplegit.__main__ import main
import sys
print(sys.argv)
sys.argv.extend('branch updatemaster'.split())
main()