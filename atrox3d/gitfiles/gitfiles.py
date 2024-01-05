import os
from abc import ABC, abstractmethod

from ..helpers.logger import get_logger

logger = get_logger(__name__)

workdir = os.getcwd()
moduledir = os.path.dirname(__file__)

class GitFile(ABC):
    def __init__(self, source=moduledir, dest=workdir) -> None:
        self.source = source
        self.dest = dest

class GitIgnore(GitFile):
    def __init__(self, source=moduledir, dest=workdir) -> None:
        super().__init__(source, dest)
        print(f'{self.source = }')
        print(f'{self.dest = }')


