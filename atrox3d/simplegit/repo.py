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
    
    def asdict(self) -> dict:
        return(asdict(self))
    
    def get_path(self) -> Path:
        '''
        converts self.path string to Path
        '''
        return Path(self.path)
    
    # def get_status(self) -> GitStatus:
    #     return get_status(self)

    # def is_dirty(self):
    #     return self.get_status().dirty
