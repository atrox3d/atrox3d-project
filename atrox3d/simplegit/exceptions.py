try:
    from .git_command import GitCommandException
except ImportError:
    from atrox3d.simplegit.git_command import GitCommandException, run

# class GitException(GitCommandException):
    # def __init__(self, gce: GitCommandException):
        # super().__init__(**vars(gce))

class GitException(Exception):
    def __init__(self, *args) -> None:
        # super().__init__(*args)
        super().__init__('\n'.join(map(str, args)))

class GitRepoNotFoundException(FileNotFoundError): pass

class GitNotARepoException(GitException): pass

class GitStatusException(GitException): pass

class GitRemoteException(GitException): pass

class GitAddException(GitException): pass

class GitCommitException(GitException): pass

class GitFetchException(GitException): pass

class GitPushException(GitException): pass

class GitPullException(GitException): pass

class GitCloneException(GitException): pass

class GitCurrentBranchException(GitException): pass

class GitSwitchException(GitException): pass

class GitInvalidCurrentBranch(GitException): pass

class GitMergeException(GitException): pass

class GitGetBranchesException(GitException): pass


if __name__ == '__main__':
    print('hello')
    try:
        run('git ciao', path='.')
    except GitCommandException as e:
        xe = GitMergeException(e)
        print(xe)
        # print(repr(xe))