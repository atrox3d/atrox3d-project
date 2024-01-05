import sys
import logging

from ..modules import logger
from . import parser
from .normalizer import normalize

log = logger.get_logger(name=__name__, level=logging.INFO)


def main():
    # get all command line parameters, excluding the first
    # params = sys.argv[1:]
    parse = parser.get_parser()
    args = parse.parse_args()

    params = args.tokens
    log.debug(f'{params=}')
    log.debug(f'{len(params)=}')
    if not len(params):
        log.fatal('missing parameters')
        exit(1)

    rules = args.replace
    log.debug(f'{rules=}')

    params = " ".join(params)
    text = normalize(params, rules)
    print(text)

if __name__ == '__main__':
    main()
