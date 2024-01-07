from .loggerformat import LogFormat
from .logformatconfigitem import LogFormatConfigItem
from .logformatconfigitem import Defaults
from .logformatconfigitem import Constants

class LoggerFormatBuilder:
    def __init__(self) -> None:
        self.items = []
    
    def _add(self, item):
        self.items.append(item)

    def add_asctime(self, width=Constants.ASCTIME_FORMAT):
        self._add(LogFormatConfigItem('asctime', width))
        return self

    def add_module(self, width=Constants.MODULE_WIDTH):
        self._add(LogFormatConfigItem('module', width))
        return self

    def add_function(self, width=Constants.FUNCNAME_WIDTH):
        self._add(LogFormatConfigItem('funcName', width))
        return self

    def add_levelname(self, width=Constants.LEVEL_WIDTH):
        self._add(LogFormatConfigItem('levelname', width))
        return self

    def add_message(self, width=None):
        self._add(LogFormatConfigItem('message', width))
        return self

    def build(self):
        if 'message' not in [item.name for item in self.items]:
            self.add_message()
        return LogFormat(*self.items)

format = LoggerFormatBuilder().add_function().add_levelname().build()
print(format)