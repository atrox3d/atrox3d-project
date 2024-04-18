import argparse

def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="simplegit",
        description="simplegit parser"
    )

    
    subparsers = parser.add_subparsers(
                                        dest='command', 
                                        help='Commands to run', 
                                        required=True
                                        )

    backup = subparsers.add_parser('backup')
    backup.add_argument('-w', '--workspace', required=True)
    backup.add_argument('-j', '--json', required=True)
    backup.add_argument('-r', '--recurse', action='store_true', default=False)

    restore = subparsers.add_parser('restore')
    restore.add_argument('-d', '--dryrun', action='store_false', default=True)
    restore.add_argument('-j', '--json', required=True)
    restore.add_argument('-p', '--destpath', required=True)
    restore.add_argument('-b', '--breakonerrors', action='store_true', 
                         default=True, help='recurse')

    return parser.parse_args()
    

print("import _options")

