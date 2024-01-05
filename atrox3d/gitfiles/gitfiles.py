import os
import shutil
from pathlib import Path

from abc import ABC, abstractmethod

from ..helpers.logger import get_logger

logger = get_logger(__name__, 'INFO')

def getpath(dirpath, filename) -> Path:
    logger.debug(f'{dirpath=}')
    logger.debug(f'{filename=}')
    return Path(dirpath) / filename

def copyfile(src: Path, dest: Path, overwrite: bool=False) -> None:
    if not src.exists():
        raise FileNotFoundError(f'source file is missing: {src}')
    
    if dest.exists() and not overwrite:
        raise FileExistsError(f'dest file exists, overwrite is disabled: {dest}')

    logger.debug(f'copy')
    logger.debug(f'{src=}')
    logger.debug(f'{dest=}')
    shutil.copy(src, dest)

def copy(copy_gitignore=True, copy_gitattributes=True) -> None:
    if copy_gitignore:
        src = getpath(os.path.dirname(__file__), '.gitignore.txt')
        dest = getpath(os.getcwd(), '.gitignore')
        copyfile(src, dest)

    if copy_gitattributes:
        src = getpath(os.path.dirname(__file__), '.gitattributes.txt')
        dest = getpath(os.getcwd(), '.gitattributes')
        copyfile(src, dest)
