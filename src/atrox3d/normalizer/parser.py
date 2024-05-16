import argparse
import sys


def get_parser():
    # create parser
    parser = argparse.ArgumentParser(
        description="test parser"
    )

    parser.add_argument('tokens', nargs='+')

    # expects argument
    # default = None
    # parser.add_argument('-o', '--option')

    parser.add_argument('-r', '--replace',
                        action='append',
                        nargs=2,
                        default=[],
                        metavar=('SEARCH', 'REPLACE'),
                        )

    return parser
