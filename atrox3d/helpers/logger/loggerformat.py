from .logformatconfigitem import LogFormatConfigItem
from . import defaults as Defaults

class LoggerFormat:
    def __init__(self, *items: list[LogFormatConfigItem], separator=' | ') -> None:
        self._items: list[LogFormatConfigItem] = list(items)
        self._separator = separator
        
        # enable dot access
        for item in items:
            setattr(self, item.name, item)
            
    
    # def __getitem__(self, name) -> LogFormatConfigItem:
    #         ''' simulate dict[access] '''
    #         for item in self._items:
    #             if item.name == name:
    #                 return item
    #         raise KeyError
    
    def __iter__(self):
        for item in self._items:
            yield item

    def __str__(self) -> str:
        return repr(self._separator.join(map(str, self)))

# default_config = LogFormat( Defaults.asctime, Defaults.module, Defaults.funcname, Defaults.level, Defaults.message ) 
default_config = LoggerFormat(*Defaults.default_list)

def main():
    for item in default_config:
        print(f'{repr(item) =}')
        print(f'{item = !s}')
        print()

    default_config.asctime.width = 15
    print(f'{default_config = !s}')

    print(f'{default_config["asctime"] = }')

if __name__ == '__main__':
    main()