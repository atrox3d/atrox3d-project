import json
from pathlib import Path
from typing import Generator

# from common import get_gitrepos
# from vscode_workspace import VsCodeWorkspace
# import options
from atrox3d.simplegit import git

def scan(*paths: str, remote :bool=None, recurse: bool=True, absolute :bool=False) -> Generator[git.GitRepo, None, None]:
    '''
    returns a generator of GitRepo objects inside the root folder
    - if recurse==True, searches recursively every git repo inside each workspace item
    - if absolute==True, the paths are converted to absolute paths
    '''
    def filter_repo(repo:git.GitRepo, remote) -> git.GitRepo | None:
        if remote is None:
            return repo
        elif remote and repo.remote:
            return repo
        elif not remote and repo.remote is None:
            return repo
        else:
            return False

    for path in paths:
        path = Path(path).resolve() if absolute else Path(path)
        if not path.exists():
            raise FileNotFoundError(path)
        
        if recurse:
            for repo_git_folder in path.glob('**/.git/'):
                repo = git.get_repo(repo_git_folder.parent)
                if filter_repo(repo, remote) is not False:
                    yield repo
        else:
            try:
                repo = git.get_repo(path)
                if filter_repo(repo, remote) is not False:
                    yield repo
            except git.NotAGitRepo:
                pass

def collect(*paths: str, recurse: bool, absolute=False) -> dict:
    # ws = VsCodeWorkspace(workspace_path)
    repos = {}
    for repo in scan(*paths, recurse=recurse, absolute=absolute, remote=True):
        print(f'ADDING | {repo.path}')
        repos[repo.path] = repo.remote
    return repos

def save(repos: dict, json_path: str):
    print(f'SAVING  | {json_path}')
    with open(json_path, 'w') as fp:
        json.dump(repos, fp, indent=2)

def load(json_path: str):
    print(f'LOADING | {json_path}')
    with open(json_path) as fp:
        repos = json.load(fp)
    return repos

def backup_repos(*paths: str, json_path:str, recurse: bool, absolute=False):
    clone = collect(*paths, recurse=recurse, absolute=absolute)
    save(clone, json_path)


def restore_repos(json_path:str, base_path: str, dryrun=True, breakonerrors=True):
    clone = load(json_path)

    for path, remote in clone.items():
        dest_path = (Path(base_path) / path).resolve()
        if dryrun:
            print(f'DRYRUN | {dest_path}')
        else:
            print(f'CLONE TO PATH | {dest_path}')
            try:
                output = git.clone(remote, dest_path)
                print(output)
            except git.GitException as ge:
                print(ge)
                if breakonerrors:
                    return


if __name__ == '__main__':
    backup_repos(
                    # r'..\..\..\zio',
                    # r'c:\users\nigga\code\php',
                    # r'c:\users\nigga\code\bash',
                    r'..\..\..\bash\..\python',
                    # r'../../../bash/../python',
                    json_path=r'C:\Users\nigga\code\vscode\repos.json',
                    recurse=True,
                    # absolute=True,
    )


