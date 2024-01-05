from .gitfiles import copy
from ..helpers.logger import get_logger

logger = get_logger(__name__)

def main():
    try:
        copy()
    except FileNotFoundError as fnfe:
        print(fnfe)
    except FileExistsError as fee:
        print(fee)

if __name__ == '__main__':
    main()
