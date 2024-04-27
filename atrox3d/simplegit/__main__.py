import os
import sys
import logging
from pathlib import Path

from . import _options
from . import git

logger = logging.getLogger(__name__)

def main():
    LOGFILE = str(Path(__file__).parent / Path(__file__).stem) + '.log'
    handlers = [
        logging.FileHandler(LOGFILE, mode='w'),
        logging.StreamHandler()
    ]

    logging.basicConfig(level='INFO', format='%(levelname)s | %(message)s', handlers=handlers)
    args = _options.parse()

    logger.info(f'{LOGFILE = }')
    logger.info(f'{args = }')
    logger.info(f'cwd = {os.getcwd()}')

    try:
        repo = git.get_repo(os.getcwd())
        
        current_branch = git.get_current_branch(repo)
        logger.info(f'{current_branch = }')
        
        status = git.get_status(repo)

        match args.command:
            case 'branch':
                match args.branch_command:
                    case 'clean':
                        # TODO: parametrize origin and master
                        if args.local:
                            logger.info('getting local branches...')
                            local_branches = git.get_branches(repo, local=True, remote=False)
                            logger.info(f'{local_branches = }')
                            for branch in local_branches:
                                if branch in ('master', current_branch):
                                    logger.info(f'skipping {branch}...')
                                else:
                                    git.delete_branch(repo, branch, local=True, force=args.force)
                        else:
                            logger.info('skipping local branches...')
                        
                        if args.remote:
                            logger.info('getting remote branches...')
                            remote_branches = git.get_branches(repo, local=False, remote=True)
                            logger.info(f'{remote_branches = }')
                            for branch in remote_branches:
                                branch = branch.removeprefix('origin/')
                                if branch == 'master':
                                    logger.info('skipping master...')
                                else:
                                    git.delete_branch(repo, branch, remote=True)
                        else:
                            logger.info('skipping remote branches...')

                    case 'updatemaster':
                        # TODO: change to update BRANCH, default=MASTER
                        # TODO: parametrize origin and master
                        
                        if status.dirty:
                            logger.info(f'ERROR | repo is dirty: commit or stash changes')
                            sys.exit(1)
                        else:
                            logger.info(f'switching to master...')
                            git.switch(repo, 'master')
                            logger.info(f'current branch: {git.get_current_branch(repo)}')
                            
                            logger.info(f'merging from {current_branch}...')
                            git.merge(repo, 'master', current_branch)

                            if args.push:
                                logger.info('pushing master...')
                                git.push(repo)

                            logger.info(f'switching back to {current_branch}...')
                            git.switch(repo, current_branch)
                            logger.info(f'current branch: {git.get_current_branch(repo)}')

                    case 'foreach':
                        raise NotImplementedError()

    except git.GitNotARepoException:
        logger.info('please run this command inside a git repo')
        sys.exit(1)
    except git.GitException as ge:
        logger.info(f'{ge.__module__}.{ge.__class__.__qualname__}: {ge}')
        sys.exit(1)
    
    