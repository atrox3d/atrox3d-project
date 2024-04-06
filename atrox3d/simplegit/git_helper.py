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
            # TODO: fix parsing
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
            case 'RM', filename, '->', newname:
                status.renamed.append(filename)
                status.added.append(newname)
            case 'D', filename:
                status.deleted.append(filename)
            case 'R', filename, '->', newname:
                status.renamed.append(filename)
                status.added.append(newname)
            case '??', filename:
                status.untracked.append(filename)
            case _:
                raise ValueError(f'unknown status {line.split()!r}')
    return status

def _format_stream(stream, prefix):
    return '\n'.join(
        [f'{prefix} | {line}' for line in stream.rstrip().split('\n')]
    )

def _run(command, path):
    try:
        result = git_command.run(command, path)
    except GitCommandException as gce:
        raise GitException(gce)
    return _format_stream(result.stdout, command) + '\n' + _format_stream(result.stderr, command)

def add(path, *files, all=False):
    command =  'git add '
    if all:
        command += '.'
    else:
        command += ' '.join(files)
    return _run(command, path)

def commit(path, comment, *files, all=False):
    command =  'git commit '
    if all:
        command += '-am '
    else:
        command += '-m '
    command +=f'\'{comment}\''
    return _run(command, path)

def push(path):
    command = 'git push'
    return _run(command, path)

def pull(path):
    command = 'git pull'
    return _run(command, path)

def clone(remote: str, dest_path: str, path: str=None):
    command = f'git clone {remote} '
    
    # shlex.split breaks on windows paths
    # https://stackoverflow.com/a/63534016
    command += str(Path(dest_path).as_posix())

    path = '.' if path is None else path
    return _run(command, path)
