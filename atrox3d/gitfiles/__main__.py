from .gitfiles import GitIgnore
from ..helpers.logger import get_logger

logger = get_logger(__name__)

def main():
    gi = GitIgnore()


if __name__ == '__main__':
    main()
