
from .logformatconfigitem import LogFormatConfigItem, Defaults

class LogFormat:
    def __init__(self, *items: list[LogFormatConfigItem], separator=' | ') -> None:
        self._items = list(items)
        for item in items:
            setattr(self, item.name, item)
        self._separator = separator
    
    def __iter__(self):
        for item in self._items:
            yield item

    def __str__(self) -> str:
        # return self._separator.join([str(item) for item in self._items])
        # items = [str(item) for name, item in vars(self).items() if not name.startswith('_')]
        return repr(self._separator.join(map(str, self)))

default_config = LogFormat(
                        Defaults.asctime, 
                        Defaults.module, 
                        Defaults.funcname, 
                        Defaults.level, 
                        Defaults.message
                        )

def main():
    # for item in [Defaults.asctime, Defaults.module, Defaults.level, Defaults.message]:
    for item in default_config:
        print(f'{repr(item) =}')
        print(f'{item = !s}')
        print()

    default_config.asctime.width = 15
    print(f'{default_config = !s}')

if __name__ == '__main__':
    main()