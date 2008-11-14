"""This module defines the logging system.

To change the logging level, assign INFO, DEBUG or ERROR to log.level. Default
is INFO.

To change the output stream, call the set_output() function. Default is
sys.stderr.
"""

import logging
import re

from time import strftime, localtime

from pythoscope.util import module_path_to_name


INFO  = logging.INFO
DEBUG = logging.DEBUG
ERROR = logging.ERROR

def path2modname(path, default=""):
    """Take a path to a pythoscope module and return a module name in dot-style
    notation. Return default if path doesn't point to a pythoscope module.

    >>> path2modname("sth/pythoscope/astvisitor.py")
    'astvisitor'
    >>> path2modname("sth/pythoscope/generator/__init__.py")
    'generator'
    >>> path2modname("sth/pythoscope/generator/adder.py")
    'generator.adder'
    """
    match = re.search(r'.*pythoscope/(.*)$', path)
    if match:
        return module_path_to_name(match.group(1), newsep=".")
    else:
        return default

class LogFormatter(logging.Formatter):
    def format(self, record):
        """Show a message with a loglevel in normal verbosity mode and much more
        in debug mode.
        """
        message = "%s: %s" % (record.levelname, record.getMessage())
        if log.level == DEBUG:
            return "%s.%d %s:%d %s" % \
                (strftime("%H%M%S", localtime(record.created)),
                 record.msecs,
                 path2modname(record.pathname, default=record.module),
                 record.lineno,
                 message)
        return message

# Don't call this "setup" or nose will assume this is the fixture setup
# function for this module.
def setup_logger():
    handler = logging.StreamHandler()
    handler.setFormatter(LogFormatter())
    log.addHandler(handler)
    log.level = INFO

def get_output():
    return log.handlers[0].stream

def set_output(stream):
    "Change the output of all the logging calls to go to given stream."
    log.handlers[0].stream = stream

log = logging.getLogger('pythoscope')
setup_logger()
