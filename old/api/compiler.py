"""
API modules that provides the base classes for adding support for a new compiler in hackedit.
"""
import functools
import copy
import json
import locale
import logging
import os
import re
import sys

from PyQt5 import QtCore, QtWidgets

from hackedit.api import system, utils
from hackedit.app import msvc, settings
from hackedit.app.forms import compiler_config_ui


def get_configs_for_mimetype(mimetype):
    """
    Gets all the possible compiler configs for the given mimetype.

    I.e. get all gcc configs, all GnuCOBOL configs,...
    """
    from hackedit.api import plugins

    def get_user_configs_for_type_name(type_name):
        ret_val = []
        for config in settings.load_compiler_configurations().values():
            if config.type_name == type_name:
                ret_val.append(config)
        return ret_val

    ret_val = []
    typenames = []
    # gets the list of compiler type names that are available for the mimetype
    for plugin in plugins.get_compiler_plugins():
        compiler = plugin.get_compiler()
        if mimetype in compiler.mimetypes:
            typenames.append(compiler.type_name)
    for type_name in typenames:
        ret_val += plugins.get_compiler_plugin_by_typename(type_name).get_auto_detected_configs()
        ret_val += get_user_configs_for_type_name(type_name)

    return ret_val



def _logger():
    return logging.getLogger(__name__)
