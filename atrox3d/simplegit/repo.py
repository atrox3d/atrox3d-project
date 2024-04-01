# from modules.simplegit.git_helper import get_status
# from modules.simplegit.status import GitStatus


from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class GitRepo:
    path: str
    remote: str = None
    name: str = None


    def __post_init__(self):
        self.path = str(self.path)
        if self.name is None:
            self.name = Path(self.path).stem
    
    def asdict(self):
        return(asdict(self))
    
    def get_path(self):
        return Path(self.path)
    
    # def get_status(self) -> GitStatus:
    #     return get_status(self)

    # def is_dirty(self):
    #     return self.get_status().dirty
