print(f'IMPORT | {__name__}')

from pathlib import Path
import re

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

def get_remote(path:str) -> str:
    '''
    extracts remote from git remote command
    '''
    try:
        result = git_command.run('git remote -v', path)
    except GitCommandException as gce:
        raise GitException(gce)

    if result.stdout:
        name, url, mode = result.stdout.split('\n')[0].split()
        return url
    else:
        return None

def get_status(repo:GitRepo) -> GitStatus:
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

    try:
        result = git_command.run(command, repo.path)
    except GitCommandException as gce:
        raise GitException(gce)

    branchstatus, *lines =  result.stdout.split('\n')
    branch_pattern = r'^## (?P<branch>[^ .]+)' \
                     r'(\.{3}(?P<remote>\S+))' \
                     r'*( \[{0,1}(?P<position>\S+) (?P<commits>\d+)\]{0,1})*$'
    
    res = re.match(branch_pattern, branchstatus)
    status = GitStatus()
    status.branch, status.remote, status.position, status.commits = res.groupdict().values()

    if status.position == 'ahead': status.need_push = True
    if status.position == 'behind': status.need_pull = True
    
    # ^(?P<index>[ ?AMDR])(?P<workspace>[ ?AMDR])\s(?P<filename>\S+)(?: -> )*(?P<newname>\S+)*$
    status_pattern = r'^(?P<index>[ ?AMDR])(?P<workspace>[ ?AMDR])' \
                     r'\s(?P<filename>\S+)(?: -> )*(?P<newname>\S+)*$'
    for line in [line for line in lines if len(line)]:
        res = re.match(status_pattern, line)
        try:
            index, workspace, filename, newname = res.groupdict().values()
        except Exception as e:
            print('-' * 80)
            print(repr(e))
            print(f'{repo = }')
            print(f'{line = }')
            print(f'{res = }')
            print('-' * 80)
            raise e
        
        status.dirty = True

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
                    status.renamed.append(filename)
                    status.added.append(newname)
                case _:
                    raise ValueError(f'unknown {flag=!r} in status {line.split()!r}')
    return status

def _format_stream(stream, prefix):
    ''' helper: returns formatted stream with prefix '''
    return '\n'.join(
        [f'{prefix} | {line}' for line in stream.rstrip().split('\n')]
    )

def _run(command, path):
    ''' helper: runs command and returns formatted stdout+stderr '''
    try:
        result = git_command.run(command, path)
    except GitCommandException as gce:
        raise GitException(gce)
    return _format_stream(result.stdout, command) + '\n' + _format_stream(result.stderr, command)

def add(path, *files, all=False):
    command =  'git add '
    command += '.' if all else ' '.join(files)
    return _run(command, path)

def commit(path, comment, add_all=False):
    command =  'git commit '
    command += '-am ' if add_all else '-m'
    command += f'\'{comment}\''
    return _run(command, path)

def push(path):
    command = 'git push'
    return _run(command, path)

def pull(path):
    command = 'git pull'
    return _run(command, path)

def clone(remote: str, dest_path: str, path: str='.'):
    command = f'git clone {remote} '
    # shlex.split breaks on windows paths
    # https://stackoverflow.com/a/63534016
    command += str(Path(dest_path).as_posix())
    return _run(command, path)
