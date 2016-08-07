import logging
import os
import re

from PyQt5 import QtCore

from hackedit.api import utils, system







def check(interpreter):
    """
    Check if the interpreter instance works. The result is cached to prevent testing configurations that have already
    been tested.

    :raises: InterpreterCheckFailedError
    """
    classname = interpreter.__class__.__name__
    json_config = interpreter.config.to_json()
    _perform_check(classname, json_config, interpreter=interpreter)


def get_version(interpreter, include_all=False):
    """
    Gets the version of the specified compiler and cache the results to prevent from running the compiler process
    uselessy.

    :returns: the compiler's version
    """
    path = interpreter.config.command
    return _get_version(path, include_all, interpreter=interpreter)


@utils.memoize_args
def _perform_check(classname, json_config, interpreter=None):
    if interpreter:
        interpreter.check()


@utils.memoize_args
def _get_version(interpreter_path, include_all, interpreter=None):
    if interpreter:
        return interpreter.get_version(include_all=include_all)
    return ''


def _logger():
    return logging.getLogger(__name__)
