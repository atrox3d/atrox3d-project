import logging
import types
from pathlib import Path
import sys

class LoggerNotFoundException(AttributeError): pass
class AlreadyConfiguredLoggingException(Exception): pass
class LoggingNotConfiguredException(Exception): pass

_IS_LOGGING_CONFIGURED = False
_ROOT_LOGGER_FORMAT = f'%(levelname)-{len("CRITICAL")}s | %(message)s'

def is_logging_configured() -> bool:
    ''' "public" getter the "private" value of flag '''
    # logging.debug(f'getting value for {_IS_LOGGING_CONFIGURED = }')
    return _IS_LOGGING_CONFIGURED

def _set_logging_configured(state: bool) -> None:
    ''' "private setter for the value of the flag '''
    global _IS_LOGGING_CONFIGURED
    _IS_LOGGING_CONFIGURED = state
    # logging.debug(f'setting value for {_IS_LOGGING_CONFIGURED = }')

def setup_logging(
                    level: int|str =logging.INFO,
                    format: str=_ROOT_LOGGER_FORMAT,
                    force: bool=True,
                    shutdown:bool=False,
                    logfile: str|Path=None,
                    caller_path: str=None,
                    **kwargs
) -> None:
    ''' configures logging if not already done '''

    if is_logging_configured() and not force:
        raise AlreadyConfiguredLoggingException(f'basicConfig already called')
    
    default_handlers = [logging.StreamHandler()]
    if logfile and caller_path:
        raise ValueError('setup_logging: only one of logfile and calle_path is allowed')
    if caller_path is not None:
        logfile = str(Path(caller_path).parent / Path(caller_path).stem) + '.log'
    if logfile is not None:
        default_handlers.append(logging.FileHandler(logfile, mode='a'))
    default_handlers.extend(kwargs.get('handlers') or [])
    
    kwargs.update(dict(
            handlers=default_handlers, 
            level=level, 
            format=format,
            force=force)
        )
    logging.debug(f'calling basicConfig with {kwargs = }')
    logging.basicConfig(**kwargs)

    _ROOT_LOGGER_FORMAT = format
    
    if shutdown:
        logging.shutdown()  # prevents unclosed file warning
    _set_logging_configured(True)
    # logging.debug('logging configured')

def shutdown_logging() -> None:
    logging.shutdown()

def get_rootlogger_format() -> str:
    return _ROOT_LOGGER_FORMAT

def add_stream(_logger:logging.Logger, stream=None, format:str=None, level: int|str =None):
    sh = logging.StreamHandler(stream)
    formatter = logging.Formatter(get_rootlogger_format())
    sh.setFormatter(formatter)
    if level:
        sh.setLevel(level)
    _logger.addHandler(sh)

def add_logfile(_logger:logging.Logger, logfile:Path|str, level: int|str =None):
    fh = logging.FileHandler(logfile)
    formatter = logging.Formatter(get_rootlogger_format())
    fh.setFormatter(formatter)
    if level:
        fh.setLevel(level)
    _logger.addHandler(fh)

def get_logger(name: str, level: int|str =None, logfile=None, configure=False) -> logging.Logger:
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
            if level is not None:
                setup_logging(level)
            else:
                setup_logging()
    
    logger = logging.getLogger(name)
    if level is not None:
        logger.setLevel(level)
    
    if logfile is not None:
        add_logfile(logger, logfile, level)
    # logging.debug(f'logging is configured: obtaining logger {logger}')
    return logger

if __name__ == '__main__':
    rootlogger = logging.getLogger()
    print(rootlogger)
    print(f'setting root logger level to DEBUG')
    rootlogger.setLevel('DEBUG')
    setup_logging(level='ERROR', caller_path=__file__)
    print(rootlogger)
    logger = get_logger(__name__)
    print(logger)
