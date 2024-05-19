
import logging
import sys
import types


def get_module_loggers(module: types.ModuleType) -> list[logging.Logger]:
    ''' return loggers for the specified module '''
    loggers = []
    for element in vars(module).values():
        if isinstance(element, logging.Logger):
            logging.debug(f'adding {element} from {module}')
            loggers.append(element)
    return loggers

def set_module_loggers_level(module: types.ModuleType, level: int|str) -> None:
    ''' sets all loggers for the specified module to level '''
    for logger in get_module_loggers(module):
        logging.debug(f'setting level {logging.getLevelName(level)} for {logger}')
        logger.setLevel(level)

def set_logger_level_for_modules(level: int|str, *modules: types.ModuleType) -> None:
    ''' sets all loggers for the specified moduleS to level '''
    for module in modules:
        set_module_loggers_level(module, level)

def set_logger_level_for_imported_modules(level: int|str, name: str) -> None:
    ''' sets all loggers for the imported modules from module "name" to level '''
    module = sys.modules[__name__]
    imported = [member for member in vars(module).values() if isinstance(member, types.ModuleType)]
    set_logger_level_for_modules(level, *imported)
