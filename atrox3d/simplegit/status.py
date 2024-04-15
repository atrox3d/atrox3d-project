from dataclasses import dataclass, field


@dataclass
class GitStatus:
    '''
    4.2. Status Flags
    Furthermore, the status flag consists of two characters. 
    If we're not performing a merge operation, 
    the first character shows the index status 
    while the second shows the workspace status.

    The above example shows four different status flags:

     M: modified
     A: Added
     D: deleted
    ??: unknown to the index

    Additionally, the -porcelain option accepts a version property with two 
    available values, 1 and 2. 
    If we don't set a value, version 1 is the default. 
    Also, version 1 is guaranteed not to change in the future 
    and is more concise than version 2. 
    As a result, it's easier and safer to use it within a script.
    '''
    branch: str = None
    remote_branch: str = None
    position: str = None
    commits: str = None
    modified: list = field(default_factory=list)
    added: list = field(default_factory=list)
    deleted: list = field(default_factory=list)
    untracked: list = field(default_factory=list)
    # unstaged: list = field(default_factory=list)
    renamed: list = field(default_factory=list)
    dirty: bool = False
    need_push: bool = False
    need_pull: bool = False

    def total(self):
        return sum(map(len, [
            self.modified, self.added, self.deleted,
            self.untracked, self.renamed
        ]))
        # return sum([len(getattr(self, l)) for l in vars(self) 
                    # if isinstance(getattr(self, l), list)])
    
# if __name__ == '__main__':
    # status = GitStatus()
    # status.added.append(1)
    # status.deleted.append(1)
    # print(status.total())