import logging

logger = logging.getLogger(__name__)
logger.debug(f"import {__name__}")

from pathlib import Path
import subprocess
import os
import shlex

class GitCommandException(subprocess.CalledProcessError):
    def __init__(self, *args, path, **kwargs):
        self.path = path
        super().__init__(*args, **kwargs)
    
    def __str__(self) -> str:
        out = []
        out.append(f'{type(self).__name__} running command {self.cmd}')
        out.append(f'PATH    : {self.path}')
        out.append(f'CMD     : {self.cmd}')
        # out.append(f'ARGS    : {self.args}')
        out.append(f'EXITCODE: {self.returncode}')
        out.append(f'STDOUT  : {self.stdout}')
        out.append(f'STDERR  : {self.stderr}')
        return '\n'.join(out)

def pushd(fn):
    def wrapper(*args, **kwargs):
        cwd = os.getcwd()
        try:
            logger.debug(f'saving {cwd = }')
            _allargs = ', '.join([str(arg) for arg in args] + [f'{k}={v}' for k, v in kwargs.items()])
            logger.debug(f'calling {fn.__name__}({_allargs})')
            result = fn(*args, **kwargs)
            return result
        finally:
            os.chdir(cwd)
    return wrapper

@pushd
def run(command:str, path:str) -> subprocess.CompletedProcess:
    logger.debug(f'changing dir to {path}')
    os.chdir(Path(path).resolve())
    # shlex.split breaks on windows paths
    # use Path(path).as_posix()
    # https://stackoverflow.com/a/63534016
    args = shlex.split(command)
    try:
        logger.debug(f'running {args}')
        completed = subprocess.run(args, check=True, shell=False, capture_output=True, text=True)
        return completed
    except subprocess.CalledProcessError as cpe:
        raise GitCommandException(**vars(cpe), path=path)
