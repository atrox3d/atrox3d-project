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
        result = fn(*args, **kwargs)
        os.chdir(cwd)
        return result
    return wrapper

@pushd
def run(command:str, path:str) -> subprocess.CompletedProcess:
    os.chdir(Path(path).resolve())
    # shlex.split breaks on windows paths
    # use Path(path).as_posix()
    # https://stackoverflow.com/a/63534016
    args = shlex.split(command)
    try:
        completed = subprocess.run(args, check=True, shell=False, capture_output=True, text=True)
        return completed
    except subprocess.CalledProcessError as cpe:
        raise GitCommandException(**vars(cpe), path=path)
