import sys
import logging

from ..helpers.logger import logger
from . import parser
log = logger.get_logger(name=__name__, level=logging.INFO)

def normalize(text: str, rules: list[list[str]]=None):
    # join alla parameters with a dash and convert everything to lowercase
    # text = "-".join(params)
    # text = text.replace(' ', '-')
    text = text.lower()

    # first rule, converto to a dash every char of this string
    dash = "-"
    to_dash = " ,;:+"

    # second rule, converto to dot every combination of dot-dash
    dot = "."
    to_dot = [".-"]  # this is considered as one

    # third rule, delete parenthesis
    nothing = ""
    to_nothing = "()[]{}"

    # dictionary of rules
    substitutions = {
        # target: replace
        dash: to_dash,
        dot: to_dot,
        nothing: to_nothing,
    }
    # add custom rules from command line
    target: str
    replace: str
    rules = rules or []
    substitutions.update({replace:target for target, replace in rules})
    log.debug(substitutions)

    # apply all the rules
    for replace, targets in substitutions.items():
        for target in targets:
            log.debug(f'replacing {target} with {replace}')
            text = text.replace(target, replace)

    # last touches: remove multiple dashes
    while "--" in text:
        text = text.replace("--", "-")
    
    text = text.lstrip('-')
    text = text.rstrip('-')

    return text
