import argparse
import sys


def get_parser():
    # create parser
    parser = argparse.ArgumentParser(
        description="test parser"
    )

    parser.add_argument('tokens', nargs='*')

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


def parse():
    return parser.parse_args()


if __name__ == '__main__':
    parser = get_parser()

    # params = [
    #     '19. Strings: Slicing'
    # ]
    params = '19. Strings: Slicing'.split()
    sys.argv.extend(params)

    args: argparse.Namespace = parser.parse_args()

    # for x, y in args.__dict__.items():
    #     print(x, y)
    for k, v in vars(args).items():
        print(f'{k} = {v}')
