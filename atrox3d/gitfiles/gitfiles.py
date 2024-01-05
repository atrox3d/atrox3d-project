import os
import shutil
from pathlib import Path

from ..helpers.logger import get_logger

logger = get_logger(__name__, 'INFO')

def copyfile(src: Path, dest: Path, overwrite: bool=False) -> None:
    if not src.exists():
        raise FileNotFoundError(f'source file is missing: {src}')
    if dest.exists() and not overwrite:
        raise FileExistsError(f'dest file exists, overwrite is disabled: {dest}')
    shutil.copy(src, dest)

def copy(copy_gitignore=True, copy_gitattributes=True) -> None:
    if copy_gitignore:
        src = Path(os.path.dirname(__file__), '.gitignore.txt')
        dest = Path(os.getcwd(), '.gitignore')
        copyfile(src, dest)

    if copy_gitattributes:
        src = Path(os.path.dirname(__file__), '.gitattributes.txt')
        dest = Path(os.getcwd(), '.gitattributes')
        copyfile(src, dest)
