from .loggerformat import LoggerFormat
from .logformatconfigitem import LogFormatConfigItem
from .logformatconfigitem import Constants

class LoggerFormatBuilder:
    def __init__(self) -> None:
        self.items = []
    
    def _add(self, item: LogFormatConfigItem):
        self.items.append(item)

    def add_asctime(self, width=None):
        self._add(LogFormatConfigItem('asctime', width))
        return self

    def add_module(self, width=Constants.MODULE_WIDTH):
        self._add(LogFormatConfigItem('module', width))
        return self

    def add_function(self, width=Constants.FUNC_WIDTH):
        self._add(LogFormatConfigItem('funcName', width))
        return self

    def add_levelname(self, width=Constants.LEVEL_WIDTH):
        self._add(LogFormatConfigItem('levelname', width))
        return self

    def add_message(self, width=None):
        self._add(LogFormatConfigItem('message', width))
        return self
    
    def add_field(self, name, width=None, fieldtype='s'):
        self._add(LogFormatConfigItem(name, width))
        return self

    def build(self) -> LoggerFormat:
        if 'message' not in [item.name for item in self.items]:
            self.add_message()
        return LoggerFormat(*self.items)

if __name__ == '__main__':
    format = LoggerFormatBuilder()\
                .add_asctime()\
                .add_function()\
                .add_levelname()\
                .add_field('test')\
                .build()
    print(format)
