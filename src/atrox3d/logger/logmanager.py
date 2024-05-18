import logging
import types
from pathlib import Path
import sys

class LoggerNotFoundException(AttributeError): pass
class AlreadyConfiguredLoggingException(Exception): pass
class LoggingNotConfiguredException(Exception): pass

_IS_LOGGING_CONFIGURED = False

def is_logging_configured() -> bool:
    ''' "public" getter the "private" value of flag '''
    logging.debug(f'getting value for {_IS_LOGGING_CONFIGURED = }')
    return _IS_LOGGING_CONFIGURED

def _set_logging_configured(state: bool):
    ''' "private setter for the value of the flag '''
    global _IS_LOGGING_CONFIGURED
    _IS_LOGGING_CONFIGURED = state
    logging.debug(f'setting value for {_IS_LOGGING_CONFIGURED = }')

def setup_logging(
                    level: int|str =logging.INFO,
                    format: str='%(levelname)5s | %(message)s',
                    logfile: str|Path=None,
                    _file_: str=None,
                    *morehandlers: logging.Handler
):
    ''' configures logging if not already done '''

    if is_logging_configured():
        raise AlreadyConfiguredLoggingException(f'basicConfig already called')
    
    handlers = [logging.StreamHandler()]
    if _file_ is not None:
        logfile = str(Path(_file_).parent / Path(_file_).stem) + '.log'
    if logfile is not None:
        handlers.append(logging.FileHandler(logfile, mode='w'))
    handlers.extend(morehandlers)

    logging.basicConfig(level=level, format=format, handlers=handlers, force=True)
    logging.shutdown()  # prevents unclosed file warning
    _set_logging_configured(True)
    logging.debug('logging configured')

def shutdown_logging():
    logging.shutdown()

def get_logger(name: str, level: int|str =None, configure=False) -> logging.Logger:
    ''' 
        get new logger for "name" with "level", 
        configures logging if specified or raises LoggingNotConfiguredException
    '''
    if not is_logging_configured():
        if not configure:
            logging.error(f'logging has not been configured')
            raise LoggingNotConfiguredException('please call setuplogging to configure logging')
        else:
            logging.warning(f'logging has not been configured')
            logging.warning('configuring default logging')
            setup_logging(level)
    
    logger = logging.getLogger(name)
    if level is not None:
        logger.setLevel(level)
    logging.debug(f'logging is configured: obtaining logger {logger}')
    return logger

def get_module_loggers(module: types.ModuleType) -> logging.Logger:
    ''' return loggers for the specified module '''
    loggers = []
    for element in vars(module).values():
        if isinstance(element, logging.Logger):
            logging.debug(f'adding {element} from {module}')
            loggers.append(element)
    return loggers

def set_module_loggers_level(module: types.ModuleType, level: int|str):
    ''' sets all loggers for the specified module to level '''
    for logger in get_module_loggers(module):
        logging.debug(f'setting level {logging.getLevelName(level)} for {logger}')
        logger.setLevel(level)

def set_logger_level_for_modules(level: int|str, *modules: types.ModuleType):
    ''' sets all loggers for the specified moduleS to level '''
    for module in modules:
        set_module_loggers_level(module, level)

def set_logger_level_for_imported_modules(level: int|str, name: str):
    ''' sets all loggers for the imported modules from module "name" to level '''
    module = sys.modules[__name__]
    imported = [member for member in vars(module).values() if isinstance(member, types.ModuleType)]
    set_logger_level_for_modules(level, *imported)

if __name__ == '__main__':
    rootlogger = logging.getLogger()
    print(rootlogger)
    setup_logging(level='INFO')
    print(rootlogger)
    logger = get_logger(__name__)
    print(logger)
    exit()
    logging.getLogger().setLevel('DEBUG')
    print('import atrox3d.simplegit.git...')
    import atrox3d.simplegit.git
    print(f'{atrox3d.simplegit.git.logger = }')
    print(f'set level of loggers in imported modules to INFO... ')
    set_logger_level_for_imported_modules('INFO', __name__)
    print(f'{atrox3d.simplegit.git.logger = }')

    get_logger(__name__, configure=True)
