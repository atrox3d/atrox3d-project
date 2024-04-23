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
        status = git.get_status(repo)

        match args.command:
            case 'branch':
                match args.branch_command:
                    case 'clean':
                        pass
                    case 'updatemaster':
                        if status.dirty:
                            print(f'ERROR | repo is dirty: commit or stash changes')
                            sys.exit(1)
                        git.switch(repo, 'master')
                        print(f'current branch: {git.get_current_branch(repo)}')
                        branches = git.get_branches(repo, local=True, remote=False)
                        print(branches)
                        git.switch(repo, current_branch)
                        print(f'current branch: {git.get_current_branch(repo)}')
                    case 'foreach':
                        pass

    except git.NotAGitRepo:
        print('please run this command inside a git repo')
        sys.exit(1)
    