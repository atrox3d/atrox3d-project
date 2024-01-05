import os
import shutil
from pathlib import Path

from abc import ABC, abstractmethod

from ..helpers.logger import get_logger

logger = get_logger(__name__, 'DEBUG')

workdir = os.getcwd()
moduledir = os.path.dirname(__file__)

class GitFile(ABC):
    @abstractmethod
    def __init__(self, sourcefile, destfile, sourcedir=moduledir, destdir=workdir) -> None:
        self.sourcedir = Path(sourcedir)
        self.destdir = Path(destdir)
        self.sourcefile = sourcefile
        self.destfile = destfile
        self.source = self.sourcedir / self.sourcefile
        self.dest = self.destdir / self.destfile
        
        logger.debug(f'{self.sourcedir = }')
        logger.debug(f'{self.destdir = }')
        logger.debug(f'{self.source = }')
        logger.debug(f'{self.dest = }')


class GitIgnore(GitFile):
    def __init__(self, source=moduledir, dest=workdir) -> None:
        super().__init__('.gitignore', source, dest)


class GitAttributes(GitFile):
    def __init__(self, source=moduledir, dest=workdir) -> None:
        super().__init__('.gitattributes', source, dest)


def gitignore():
        return GitIgnore()