from atrox3d.normalizer import normalize

print(normalize(' jh kjh kjh kh '))

from atrox3d.simplegit import git

repo = git.get_repo('.')
status = git.get_status(repo)