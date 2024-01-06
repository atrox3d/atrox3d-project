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

def main():
    for item in [asctime, module, level]:
        print(repr(item))
        print(item)

if __name__ == '__main__':
    main()