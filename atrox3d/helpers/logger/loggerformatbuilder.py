from .loggerformat import LoggerFormat
from .logformatconfigitem import LogFormatConfigItem
from .logformatconfigitem import Constants

class LoggerFormatBuilder:
    def __init__(self) -> None:
        self.items = []
    
    def add_item(self, item: LogFormatConfigItem):
        self.items.append(item)
    
    def add_field(self, name, width=None, fieldtype='s'):
        item = LogFormatConfigItem(name, width, fieldtype)
        self.add_item(item)
        return self
    
    def add_asctime(self, width=None):
        return self.add_field('asctime', width)

    def add_module(self, width=Constants.MODULE_WIDTH):
        return self.add_field('module', width)

    def add_function(self, width=Constants.FUNC_WIDTH):
        return self.add_field('funcName', width)

    def add_levelname(self, width=Constants.LEVEL_WIDTH):
        return self.add_field('levelname', width)

    def add_message(self, width=None):
        return self.add_field('message', width)

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
