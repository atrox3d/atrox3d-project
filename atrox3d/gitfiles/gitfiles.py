import os
import shutil
from pathlib import Path

from ..helpers.logger.logger import get_logger

logger = get_logger(__name__, 'INFO')

SOURCE_DIR = os.path.dirname(__file__)
DEST_DIR = os.getcwd()

def _copyfile(src: Path, dest: Path, overwrite: bool=False) -> None:
    logger.info('COPY')
    logger.info(f'{src=!s}')
    logger.info(f'{dest=!s}')
    if not src.exists():
        raise FileNotFoundError(f'source file is missing: {src}')
    if dest.exists() and not overwrite:
        raise FileExistsError(f'dest file exists, overwrite is disabled: {dest}')
    shutil.copy(src, dest)

def copyfiles(gitignore=True, gitattributes=True) -> None:
    try:
        if gitignore:
            src = Path(SOURCE_DIR, '.gitignore.txt')
            dest = Path(DEST_DIR, '.gitignore')
            _copyfile(src, dest)
    except FileExistsError as fee:
        print(fee)

    try:
        if gitattributes:
            src = Path(SOURCE_DIR, '.gitattributes.txt')
            dest = Path(DEST_DIR, '.gitattributes')
            _copyfile(src, dest)
    except FileExistsError as fee:
        print(fee)
