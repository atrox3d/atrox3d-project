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
        branch = git.get_current_branch(repo)
        print(f'{branch = }')
        match args.command:
            case 'branch':
                match args.branch_command:
                    case 'clean':
                        pass
                    case 'updatemaster':
                        pass
                    case 'foreach':
                        pass

    except git.NotAGitRepo:
        print('please run this command inside a git repo')
        sys.exit(1)
    