import json
from pathlib import Path
from typing import Generator
import logging

logger = logging.getLogger(__name__)
logger.debug(f"import {__name__}")
# from common import get_gitrepos
# from vscode_workspace import VsCodeWorkspace
# import options
from . import git

def scan(*paths: str, has_remote :bool=None, recurse: bool=True, absolute :bool=False) -> Generator[git.GitRepo, None, None]:
    args = ', '.join([f"{k}={v}" for k, v in locals().items()])
    logger.debug(f'{args = }')
    '''
    returns a generator of GitRepo objects inside the root folder
    - if recurse==True, searches recursively every git repo inside each workspace item
    - if absolute==True, the paths are converted to absolute paths
    - if has_remote is None, returns any repo
    - if has_remote is True, returns only repos with remote
    - if has_remote is False, returns only repos without remote
    '''
    def filter_repo(repo:git.GitRepo, has_remote: bool) -> git.GitRepo | None:
        if has_remote is None:
            return repo
        elif has_remote and repo.remote is not None:
            return repo
        elif not has_remote and repo.remote is None:
            return repo
        else:
            return None

    for path in paths:
        path = Path(path).resolve() if absolute else Path(path)
        logger.debug(f'checking {path = }')
        if not path.exists():
            raise FileNotFoundError(path)
        
        if recurse:
            logger.debug(f'recurse enabled: scanning all subdir of {path}')
            for repo_git_folder in path.glob('**/.git/'):
                repo = git.get_repo(repo_git_folder.parent.as_posix())
                if filter_repo(repo, has_remote) is not None:
                    yield repo
        else:
            try:
                logger.debug(f'recurse disabled: scanning {path}')
                repo = git.get_repo(path)
                if filter_repo(repo, has_remote) is not None:
                    yield repo
            except git.GitNotARepoException:
                pass

def collect(*paths: str, recurse: bool, absolute=False) -> dict:
    # ws = VsCodeWorkspace(workspace_path)
    repos = {}
    for repo in scan(*paths, recurse=recurse, absolute=absolute, has_remote=True):
        logger.info(f'ADDING | {repo.path}')
        repos[repo.path] = repo.remote
    return repos

def save(repos: dict, json_path: str):
    logger.info(f'SAVING  | {json_path}')
    with open(json_path, 'w') as fp:
        json.dump(repos, fp, indent=2)

def load(json_path: str):
    logger.info(f'LOADING | {json_path}')
    with open(json_path) as fp:
        repos = json.load(fp)
    return repos

def backup(*paths: str, json_path:str, recurse: bool, absolute=False):
    clone = collect(*paths, recurse=recurse, absolute=absolute)
    save(clone, json_path)


def restore(json_path:str, base_path: str, dryrun=True, breakonerrors=True):
    clone = load(json_path)

    for path, remote in clone.items():
        path = Path(path).as_posix()
        dest_path: Path  = (Path(base_path) / path).resolve()
        # print(dest_path)
        # dest_path.mkdir()



        # continue
        if dest_path.exists():
            logger.info(f'SKIPPING | {dest_path!r} already exists')
        if dryrun:
            logger.info(f'DRYRUN | CLONE TO PATH | {dest_path!r}')
        else:
            logger.info(f'CLONE TO PATH | {dest_path.resolve()}')
            try:
                output = git.clone(remote, dest_path)
                logger.info(output)
            except git.GitException as ge:
                logger.error(ge)
                if breakonerrors:
                    return


if __name__ == '__main__':
    JSON = r'C:\Users\nigga\code\vscode\repos.json'

    backup(
                    # r'..\..\..\bash\..\python',
                    r'..\..\..\zio',
                    json_path=JSON,
                    recurse=True,
    )

    restore(JSON, r'd:')
