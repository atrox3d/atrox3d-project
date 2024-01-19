from .gitfiles import copyfiles
from ..helpers.logger.logger import get_logger

logger = get_logger(__name__)

def main():
    try:
        copyfiles()
    except FileNotFoundError as fnfe:
        print(fnfe)
    except FileExistsError as fee:
        print(fee)

if __name__ == '__main__':
    main()
