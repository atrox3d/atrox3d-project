print(f'IMPORT | {__name__}')

from pathlib import Path
import re

from .repo import GitRepo
from .status import GitStatus

from . import git_command
from .git_command import GitCommandException

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
    result = git_command.run('git remote -v', path)
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
    '''
    command = 'git status --branch --porcelain'
    result = git_command.run(command, repo.path)

    branchstatus, *lines =  result.stdout.split('\n')
    branch_pattern = r'^## ([^ .]+)(\.{3}(\S+))*( \[{0,1}(\S+) (\d+)\]{0,1})*$'
    res = re.match(branch_pattern, branchstatus).groups()
    status = GitStatus()
    status.branch, _, status.remote, _, status.position, status.commits = res

    if status.position == 'ahead':
        status.push = True
    elif status.position == 'behind':
        status.pull = True
    
    for line in [line for line in lines if len(line)]:
        status.dirty = True
        match line.split():
            case 'A', filename:
                status.added.append(filename)
            case 'M', filename:
                status.modified.append(filename)
            case 'AM', filename:
                status.modified.append(filename)
                status.added.append(filename)
            case 'MM', filename:
                status.modified.append(filename)
                status.unstaged.append(filename)
            case 'D', filename:
                status.deleted.append(filename)
            case '??', filename:
                status.untracked.append(filename)
            case _:
                raise ValueError(f'unknown status {line!r}')
    return status

def _format_stream(stream, prefix):
    return '\n'.join(
        [f'{prefix} | {line}' for line in stream.rstrip().split('\n')]
    )

def add(path, *files, all=False):
    command =  'git add '
    if all:
        command += '.'
    else:
        command += ' '.join(files)
    result = git_command.run(command, path)
    return _format_stream(result.stdout, command)

def commit(path, comment, *files, all=False):
    command =  'git commit '
    if all:
        command += '-am '
    else:
        command += '-m '
    command +=f'\'{comment}\''
    result = git_command.run(command, path)
    return _format_stream(result.stdout, command)

def push(path):
    command = 'git push'
    result = git_command.run(command, path)
    return _format_stream(result.stdout, command)

def pull(path):
    command = 'git pull'
    result = git_command.run(command, path)
    return _format_stream(result.stdout, command)