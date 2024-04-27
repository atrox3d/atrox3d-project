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
                        # TODO: parametrize origin and master
                        if args.local:
                            print('getting local branches...')
                            local_branches = git.get_branches(repo, local=True, remote=False)
                            print(f'{local_branches = }')
                            for branch in local_branches:
                                if branch in ('master', current_branch):
                                    print(f'skipping {branch}...')
                                else:
                                    git.delete_branch(repo, branch, local=True, force=args.force)
                        else:
                            print('skipping local branches...')
                        
                        if args.remote:
                            print('getting remote branches...')
                            remote_branches = git.get_branches(repo, local=False, remote=True)
                            print(f'{remote_branches = }')
                            for branch in remote_branches:
                                branch = branch.removeprefix('origin/')
                                if branch == 'master':
                                    print('skipping master...')
                                else:
                                    git.delete_branch(repo, branch, remote=True)
                        else:
                            print('skipping remote branches...')

                    case 'updatemaster':
                        if status.dirty:
                            print(f'ERROR | repo is dirty: commit or stash changes')
                            sys.exit(1)
                        else:
                            print(f'switching to master...')
                            git.switch(repo, 'master')
                            print(f'current branch: {git.get_current_branch(repo)}')
                            
                            print(f'merging from {current_branch}...')
                            git.merge(repo, 'master', current_branch)

                            if args.push:
                                print('pushing master...')
                                git.push(repo)

                            print(f'switching back to {current_branch}...')
                            git.switch(repo, current_branch)
                            print(f'current branch: {git.get_current_branch(repo)}')

                    case 'foreach':
                        raise NotImplementedError()

    except git.GitNotARepoException:
        print('please run this command inside a git repo')
        sys.exit(1)
    except git.GitException as ge:
        print(f'{ge.__module__}.{ge.__class__.__qualname__}: {ge}')
        sys.exit(1)
    
    