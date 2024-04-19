import os
import sys

from . import _options
from . import git

def main():
    args = _options.parse()

    print(f'{args = }')
    print(f'{os.getcwd()}')

    try:
        repo = git.get_repo(os.getcwd())
        current_branch = git.get_current_branch(repo)
        print(f'{current_branch = }')

        match args.command:
            case 'branch':
                match args.branch_command:
                    case 'clean':
                        pass
                    case 'updatemaster':
                        branches = git.get_branches(repo, local=True, remote=False)
                        print(branches)
                    case 'foreach':
                        pass

    except git.NotAGitRepo:
        print('please run this command inside a git repo')
        sys.exit(1)
    