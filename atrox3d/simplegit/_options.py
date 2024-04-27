import argparse

def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="simplegit",
        description="simplegit parser"
    )

    # expect a command as first argument (branch, repo)
    command = parser.add_subparsers(dest='command', help='Commands to run', 
                                    required=True)
    
    # expect a subcommand as second argument (clean, updatemaster, foreach)
    branch = command.add_parser('branch')
    branch_command = branch.add_subparsers(dest='branch_command', help='Commands to run', 
                                            required=True)
    clean = branch_command.add_parser('clean')
    clean.add_argument('-r', '--remote', action='store_true')
    clean.add_argument('-l', '--local', action='store_true')
    clean.add_argument('-f', '--force', action='store_true')

    updatemaster = branch_command.add_parser('updatemaster')
    updatemaster.add_argument('-P', '--push', action='store_true')
    
    foreach = branch_command.add_parser('foreach')
    foreach.add_argument('foreach', nargs='+')
    # branch.add_argument('-w', '--workspace', required=True)
    # branch.add_argument('-j', '--json', required=True)
    # branch.add_argument('-r', '--recurse', action='store_true', default=False)



    repo =  command.add_parser('repo')
    # repo.add_argument('-d', '--dryrun', action='store_false', default=True)
    # repo.add_argument('-j', '--json', required=True)
    # repo.add_argument('-p', '--destpath', required=True)
    # repo.add_argument('-b', '--breakonerrors', action='store_true', 
                        #  default=True, help='recurse')

    # return parser.parse_known_args()
    return parser.parse_args()
    

print("import _options")

