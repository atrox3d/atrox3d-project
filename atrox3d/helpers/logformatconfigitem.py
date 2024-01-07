from dataclasses import dataclass

@dataclass
class LogFormatConfigItem:
    name: str
    width: int = None
    format: str = None
    enabled: bool = True    # remove

    def __str__(self) -> str:
        width =  self.width and str(self.width) or ''
        return f'%({self.name}){width}s'

class Constants:
    ASCTIME_FORMAT='%Y/%m/%d %H:%M:%S'
    MODULE_WIDTH = 12
    FUNCNAME_WIDTH = 12
    LEVEL_WIDTH=len('CRITICAL')

class Defaults:
    asctime = LogFormatConfigItem('asctime', format=Constants.ASCTIME_FORMAT)
    module = LogFormatConfigItem('module', width=Constants.MODULE_WIDTH)
    funcname = LogFormatConfigItem('funcName', width=Constants.FUNCNAME_WIDTH)
    level = LogFormatConfigItem('levelname', width=Constants.LEVEL_WIDTH)
    message = LogFormatConfigItem('message')
