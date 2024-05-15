import logging
import types
from pathlib import Path
import sys


_IS_LOGGING_CONFIGURED = False

class LoggerNotFoundException(AttributeError): pass
class AlreadyConfiguredLoggingException(Exception): pass
class LoggingNotConfiguredException(Exception): pass

def is_logging_configured() -> bool:
    return _IS_LOGGING_CONFIGURED


def setup_logging(
                    root_level: int|str =logging.INFO,
                    format: str='%(levelname)5s | %(message)s'
) -> logging.Logger:
    global _IS_LOGGING_CONFIGURED

    if is_logging_configured():
        raise AlreadyConfiguredLoggingException(f'basicConfig already called')
    
    LOGFILE = str(Path(__file__).parent / Path(__file__).stem) + '.log'
    handlers = [
        logging.FileHandler(LOGFILE, mode='w'),
        logging.StreamHandler()
    ]

    logging.basicConfig(level=root_level, format=format, handlers=handlers)
    _IS_LOGGING_CONFIGURED = True
    logging.info('logging configured')

def get_logger(name: str, level: int|str =logging.INFO, configure=False) -> logging.Logger:
    if not is_logging_configured():
        if not configure:
            raise LoggingNotConfiguredException('please call setuplogging to configure logging')
        else:
            setup_logging(level)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logging.info(f'logging already configured: obtaining logger {logger}')
    return logger

def get_module_loggers(module: types.ModuleType) -> logging.Logger:
    loggers = []
    for element in vars(module).values():
        if isinstance(element, logging.Logger):
            loggers.append(element)
    return loggers

def set_module_loggers_level(module: types.ModuleType, level: int|str):
    for logger in get_module_loggers(module):
        logger.setLevel(level)

def set_logger_level_for_modules(level: int|str, *modules: types.ModuleType):
    for module in modules:
        set_module_loggers_level(module, level)

def set_logger_level_for_imported_modules(level: int|str, name: str):
    module = sys.modules[__name__]
    imported = [member for member in vars(module).values() if isinstance(member, types.ModuleType)]
    set_logger_level_for_modules(level, *imported)

if __name__ == '__main__':
    print('import atrox3d.simplegit.git...')
    import atrox3d.simplegit.git
    print(f'{atrox3d.simplegit.git.logger = }')
    print(f'set level of loggers in imported modules to INFO... ')
    set_logger_level_for_imported_modules('INFO', __name__)
    print(f'{atrox3d.simplegit.git.logger = }')

    get_logger(__name__, configure=True)