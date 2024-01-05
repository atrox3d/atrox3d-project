import os
import shutil
from pathlib import Path

from abc import ABC, abstractmethod

from ..helpers.logger import get_logger

logger = get_logger(__name__, 'DEBUG')

workdir = os.getcwd()
moduledir = os.path.dirname(__file__)

class GitFile(ABC):
    def __init__(self, sourcedir=moduledir, destdir=workdir) -> None:
        self.sourcedir = Path(sourcedir)
        self.destdir = Path(destdir)
        logger.debug(f'{self.sourcedir = }')
        logger.debug(f'{self.destdir = }')

class GitIgnore(GitFile):
    def __init__(self, source=moduledir, dest=workdir) -> None:
        super().__init__(source, dest)
        self.filename = '.gitignore'
        self.source = self.sourcedir / self.filename
        self.dest = self.destdir / self.filename
        logger.debug(f'{self.source = }')
        logger.debug(f'{self.dest = }')
    