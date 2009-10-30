
import re

def any_match(expressions, value):
    """
    Return true if any expression matches the value
    """
    for exp in expressions:
        if re.match(exp, str(value)):
            return True
    return False

def any_match_set(expressions, values):
    """
    Return true if any expression matches any of the values
    """
    for value in values:
        if any_match(expressions, value):
            return True
    return False

