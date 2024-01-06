from dataclasses import dataclass

@dataclass
class LogConfigItem:
    name: str
    width: int = None
    format: str = None
    enabled: bool = True    # remove

    def __str__(self) -> str:
        width =  self.width and str(self.width) or ''
        return f'%({self.name}){width}s'

asctime = LogConfigItem('asctime', format='%Y/%m/%d %H:%M:%S')
module = LogConfigItem('module', width=12)
function = LogConfigItem('funcName', width=12)
level = LogConfigItem('levelname', width=len('CRITICAL'))
message = LogConfigItem('message')

class LogFormat:
    def __init__(self, *items: list[LogConfigItem], separator=' | ') -> None:
        self._items = list(items)
        for item in items:
            setattr(self, item.name, item)
        self._separator = separator

    def __str__(self) -> str:
        # return self._separator.join([str(item) for item in self._items])
        items = [str(item) for name, item in vars(self).items() if not name.startswith('_')]
        return self._separator.join(items)

default_config = LogFormat(asctime, module, function, level, message)

def main():
    for item in [asctime, module, level, message]:
        print(repr(item))
        print(item)

    default_config.asctime.width = 15
    print(f'{default_config}')
if __name__ == '__main__':
    main()