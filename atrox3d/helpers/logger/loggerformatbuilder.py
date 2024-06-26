from .loggerformat import LoggerFormat
from .logformatconfigitem import LogFormatConfigItem
from . import constants as CONST

class LoggerFormatBuilder:
    def __init__(self) -> None:
        self.items = []
    
    def append_item(self, item: LogFormatConfigItem):
        self.items.append(item)
    
    def add_item(self, name, width=None, fieldtype='s'):
        item = LogFormatConfigItem(name, width, fieldtype)
        self.append_item(item)
        return self
    
    def add_asctime(self, width=None):
        return self.add_item('asctime', width)

    def add_module(self, width=CONST.MODULE_WIDTH):
        return self.add_item('module', width)

    def add_function(self, width=CONST.FUNC_WIDTH):
        return self.add_item('funcName', width)

    def add_levelname(self, width=CONST.LEVEL_WIDTH):
        return self.add_item('levelname', width)

    def add_message(self, width=None):
        return self.add_item('message', width)

    def build(self) -> LoggerFormat:
        if 'message' not in [item.name for item in self.items]:
            self.add_message()
        return LoggerFormat(*self.items)

if __name__ == '__main__':
    format = LoggerFormatBuilder()\
                .add_asctime()\
                .add_function()\
                .add_levelname()\
                .add_item('test')\
                .build()
    print(format)
