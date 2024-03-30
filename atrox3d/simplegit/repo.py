# from modules.simplegit.git_helper import get_status
# from modules.simplegit.status import GitStatus


from dataclasses import dataclass
from pathlib import Path


@dataclass
class GitRepo:
    name: str
    path: Path
    remote: str = None

    # def get_status(self) -> GitStatus:
    #     return get_status(self)

    # def is_dirty(self):
    #     return self.get_status().dirty
