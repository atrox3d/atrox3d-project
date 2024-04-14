import json
from pathlib import Path

# from common import get_gitrepos
# from vscode_workspace import VsCodeWorkspace
# import options
from atrox3d.simplegit import git

def scan(*paths: str, recurse: bool, absolute=False) -> dict:
    '''
    returns a generator of GitRepo objects inside the root folder
    - if recurse==True, searches recursively every git repo inside each workspace item
    - if absolute==True, the paths are converted to absolute paths
    '''
    for name, path in ws.get_configtuples():
        path = Path(path).resolve() if absolute else Path(path)
        if recurse:
            for repo_git_folder in path.glob('**/.git/'):
                yield git.get_repo(repo_git_folder.parent, name=name)
        else:
            try:
                yield git.get_repo(path, name=name)
            except git.NotAGitRepo:
                pass

if __name__ == '__main__':
    # repos = Repos(r'c:\users\nigga\code')
    # print(repos)
    # print(list(repos.repos))
    exit()

# def get_repos(path: str, recurse: bool) -> dict:
#     # ws = VsCodeWorkspace(workspace_path)
#     repos = {}
#     for repo in get_gitrepos(ws, recurse=recurse):
#         if repo.remote is not None:
#             print(f'ADDING | {repo.path}')
#             repos[repo.path] = repo.remote
#         else:
#             print(f'NO REMOTE | skipping | {repo.path}')
    
#     return repos

def save_repos(repos: dict, json_path: str):
    print(f'SAVING  | {json_path}')
    with open(json_path, 'w') as fp:
        json.dump(repos, fp, indent=2)

def load_repos(json_path: str):
    print(f'LOADING | {json_path}')
    with open(json_path) as fp:
        repos = json.load(fp)
    return repos

def backup_repos(workspace_path: str, json_path:str, recurse: bool):
    clone = get_repos(workspace_path, recurse)
    save_repos(clone, json_path)


def restore_repos(json_path:str, base_path: str, dryrun=True, breakonerrors=True):
    clone = load_repos(json_path)

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

# def main():
#     import argparse
#     parser = options.get_clone_parser()
#     args: argparse.Namespace = parser.parse_args()

#     for k, v in vars(args).items():
#         print(f'PARAM  | {k} = {v}')

#     if args.command == 'backup':
#         backup_repos(args.workspace, args.json, args.recurse)
#     elif args.command == 'restore':
#         restore_repos(args.json, args.destpath, args.dryrun, args.breakonerrors)
#     else:
#         # this should never run, because argparse takes care of it
#         raise ValueError(f'uknown subcommand {args.command!r}')



