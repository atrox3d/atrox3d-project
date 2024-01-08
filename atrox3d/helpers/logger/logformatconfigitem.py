from dataclasses import dataclass

from . import constants as CONST

@dataclass
class LogFormatConfigItem:
    name: str
    width: int = None
    fieldtype: str = 's'

    def __str__(self) -> str:
        width =  self.width and str(self.width) or ''
        return f'%({self.name}){width}{self.fieldtype}'

class Defaults:
    asctime = LogFormatConfigItem('asctime')
    module = LogFormatConfigItem('module', width=CONST.MODULE_WIDTH)
    funcname = LogFormatConfigItem('funcName', width=CONST.FUNC_WIDTH)
    level = LogFormatConfigItem('levelname', width=CONST.LEVEL_WIDTH)
    message = LogFormatConfigItem('message')

    def __iter__(self):
        for item in self._getlist():
            yield item

    def _getlist(self):
        return [getattr(self, atr) for atr in dir(self) if not atr.startswith('_')]
    
