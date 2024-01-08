from dataclasses import dataclass

@dataclass
class LogFormatConfigItem:
    name: str
    width: int = None
    fieldtype: str = 's'

    def __str__(self) -> str:
        width =  self.width and str(self.width) or ''
        return f'%({self.name}){width}{self.fieldtype}'

class Constants:
    DATE_FORMAT='%Y/%m/%d %H:%M:%S'
    ASCTIME = 'asctime'
    ASCTIME_WIDTH = len(DATE_FORMAT)
    MODULE = 'module'
    MODULE_WIDTH = 12
    FUNC = 'funcName'
    FUNC_WIDTH = 12
    LEVEL = 'levelname'
    LEVEL_WIDTH=len('CRITICAL')

class Defaults:
    asctime = LogFormatConfigItem('asctime')
    module = LogFormatConfigItem('module', width=Constants.MODULE_WIDTH)
    funcname = LogFormatConfigItem('funcName', width=Constants.FUNC_WIDTH)
    level = LogFormatConfigItem('levelname', width=Constants.LEVEL_WIDTH)
    message = LogFormatConfigItem('message')

    def __iter__(self):
        for item in self._getlist():
            yield item

    def _getlist(self):
        return [getattr(self, atr) for atr in dir(self) if not atr.startswith('_')]
    
