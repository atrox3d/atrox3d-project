from .gitfiles import gitignore
from ..helpers.logger import get_logger

logger = get_logger(__name__)

def main():
    gi = gitignore()


if __name__ == '__main__':
    main()
