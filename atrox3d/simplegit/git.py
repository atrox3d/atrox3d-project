# print(f'IMPORT | {__name__}')

from pathlib import Path
import re
import sys

from .repo import GitRepo
from .status import GitStatus

from . import git_command
from .git_command import GitCommandException

class GitException(GitCommandException):
    def __init__(self, gce: GitCommandException):
        super().__init__(**vars(gce))

class NotAGitRepo(Exception):
    pass

def get_repo(path:str, name=None) -> GitRepo:
    '''
    factory method, creates GitRepo object from path
    '''
    if is_repo(path):
        remote = get_remote(path)
        repo = GitRepo(path, remote, name=name)
        return repo
    raise NotAGitRepo(f'path {path} is not a git repo')

def is_repo(path:str) -> bool:
    repodir =  Path(path)
    if repodir.exists():
        gitdir = repodir / '.git'
        return gitdir.is_dir()
    raise FileNotFoundError(f'is_repo: {repodir} does not exist')

def __parse_status_filename(line:str, repo:GitRepo):
    # ^(?P<index>[ ?AMDR])(?P<workspace>[ ?AMDR])\s(?P<filename>\S+)(?: -> )*(?P<newname>\S+)*$
    status_pattern = r'^(?P<index>[ ?AMDR])(?P<workspace>[ ?AMDR])' \
                     r'\s(?P<filename>\S+)(?: -> )*(?P<newname>\S+)*$'
    res = re.match(status_pattern, line)
    try:
        index, workspace, filename, newname = res.groupdict().values()
        return index, workspace, filename, newname
    except Exception as e:
        import traceback
        print('-' * 80)
        print(repr(e))
        print(traceback.format_exc())
        print(f'{repo = }')
        print(f'{line = }')
        print(f'{res = }')
        print('-' * 80)
        sys.exit()

def _parse_status_filename(line:str):
    index = workspace = rest = filename = newname = None
    index, workspace = line[:2]
    rest = line[3:]
    if '->' in rest:
        filename, new = rest.split(' -> ')
    else:
        filename = rest

    return index, workspace, filename, newname
        
def get_status(path_or_repo:str|GitRepo) -> GitStatus:
    '''
    factory method, creates GitStatus object from git status command

    git status --branch --porcelain
    ## master...origin/master [ahead 4]
    M modules/git_helper.py

    https://www.baeldung.com/linux/git-script-check-clean-directory#2-status-flags
    the first character shows the index status while the second shows 
    the workspace status
    '''
    command = 'git status --branch --porcelain'
    path = path_or_repo.path if isinstance(path_or_repo, GitRepo) else path_or_repo
    try:
        result = git_command.run(command, path)
    except GitCommandException as gce:
        raise GitException(gce)

    branchstatus, *lines =  result.stdout.split('\n')
    branch_pattern = r'^## (?P<branch>[^ .]+)' \
                     r'(\.{3}(?P<remote>\S+))' \
                     r'*( \[{0,1}(?P<position>\S+) (?P<commits>\d+)\]{0,1})*$'
    
    res = re.match(branch_pattern, branchstatus)
    status = GitStatus()
    status.branch, status.remote_branch, status.position, status.commits = res.groupdict().values()

    if status.position == 'ahead': status.need_push = True
    if status.position == 'behind': status.need_pull = True
    
    for line in [line for line in lines if len(line)]:
        status.dirty = True

        index, workspace, filename, newname = _parse_status_filename(line)

        if index + workspace == '??':
            status.untracked.append(filename)
            continue
        for flag in index, workspace:
            match flag:
                case ' ':
                    pass
                case 'A':
                    status.added.append(filename)
                case 'M':
                    status.modified.append(filename)
                case 'D':
                    status.deleted.append(filename)
                case 'R':
                    # status.deleted.append(filename)
                    status.renamed.append((filename, newname))
                case _:
                    raise ValueError(f'unknown {flag=!r} in status {line.split()!r}')
    return status


def _run(command, path_or_repo:str|GitRepo) -> str:
    ''' helper: runs command and returns formatted stdout+stderr '''

    def _format_stream(stream, prefix) -> str:
        ''' helper: returns formatted stream with prefix '''
        return '\n'.join(
            [f'{prefix} | {line}' for line in stream.rstrip().split('\n')]
        )

    path = path_or_repo.path if isinstance(path_or_repo, GitRepo) else path_or_repo
    try:
        result = git_command.run(command, path)
    except GitCommandException as gce:
        raise GitException(gce)
    return _format_stream(result.stdout, command) + '\n' + _format_stream(result.stderr, command)

def get_remote(path_or_repo:str|GitRepo) -> str:
    '''
    extracts remote from git remote command
    '''
    try:
        path = path_or_repo.path if isinstance(path_or_repo, GitRepo) else path_or_repo
        result = git_command.run('git remote -v', path)
    except GitCommandException as gce:
        raise GitException(gce)

    if result.stdout:
        name, url, mode = result.stdout.split('\n')[0].split()
        return url
    else:
        return None

def get_current_branch(path_or_repo:str|GitRepo) -> str:
    '''
    extracts remote from git remote command
    '''
    try:
        command = 'git branch --show-current'
        path = path_or_repo.path if isinstance(path_or_repo, GitRepo) else path_or_repo
        result = git_command.run(command, path)
        return result.stdout.strip()
    except GitCommandException as gce:
        raise GitException(gce)

def add(path_or_repo:str|GitRepo, *files:str, all:bool=False) -> str:
    command =  'git add '
    command += '.' if all else ' '.join(files)
    return _run(command, path_or_repo)

def commit(path_or_repo:str|GitRepo, comment:str, add_all:bool=False) -> str:
    command =  'git commit '
    command += '-am ' if add_all else '-m'
    command += f'\'{comment}\''
    return _run(command, path_or_repo)

def fetch(path_or_repo:str|GitRepo) -> str:
    command = 'git fetch'
    return _run(command, path_or_repo)

def push(path_or_repo:str|GitRepo) -> str:
    command = 'git push'
    return _run(command, path_or_repo)

def pull(path_or_repo:str|GitRepo) -> str:
    command = 'git pull'
    return _run(command, path_or_repo)

def clone(remote: str, dest_path: str, path: str='.') -> str:
    command = f'git clone {remote} '
    # shlex.split breaks on windows paths
    # https://stackoverflow.com/a/63534016
    command += str(Path(dest_path).as_posix())
    return _run(command, path)
