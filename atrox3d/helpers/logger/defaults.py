from .logformatconfigitem import LogFormatConfigItem
from . import constants as CONST

asctime = LogFormatConfigItem('asctime')
module = LogFormatConfigItem('module', width=CONST.MODULE_WIDTH)
funcname = LogFormatConfigItem('funcName', width=CONST.FUNC_WIDTH)
level = LogFormatConfigItem('levelname', width=CONST.LEVEL_WIDTH)
message = LogFormatConfigItem('message')

default_list = [
    asctime,
    module,
    funcname,
    level,
    message,
]
