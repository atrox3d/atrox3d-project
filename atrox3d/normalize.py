import sys
import logging

from modules import logger
from modules import parser

DEBUG = False
log = logger.get_logger(
                    name=__name__,
                    level=logging.INFO
)

# get all command line parameters, excluding the first
# params = sys.argv[1:]
parser = parser.get_parser()
args = parser.parse_args()

params = args.tokens
log.debug(f'{params=}')
log.debug(f'{len(params)=}')
if not len(params):
    log.fatal('missing parameters')
    exit(1)

rules = args.replace
log.debug(f'{rules=}')

# join alla parameters with a dash and convert everything to lowercase
text = "-".join(params)
text = text.lower()

# first rule, converto to a dash every char of this string
dash = "-"
to_dash = " ,;:"

# second rule, converto to dot every combination of dot-dash
dot = "."
to_dot = [".-"]  # this is considered as one

# third rule, delete parenthesis
nothing = ""
to_nothing = "()[]{}"

# dictionary of rules
substitutions = {
    dash: to_dash,
    dot: to_dot,
    nothing: to_nothing,
}
# add custom rules from command line
for target, replace in rules:
    substitutions[replace] = target
log.debug(substitutions)

# apply all the rules
for replace, targets in substitutions.items():
    for target in targets:
        log.debug(f'replacing {target} with {replace}')
        text = text.replace(target, replace)

# last touch: remove multiple dashes
while "--" in text:
    text = text.replace("--", "-")

# prints the final string, ready to be processed by the shell
print(text)
