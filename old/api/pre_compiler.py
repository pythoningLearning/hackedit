"""
API modules that provides the base classes for adding support for a new pre-compiler in hackedit.

A pre-compiler is any tool that convert a source file of some type to a source file of another type (e.g. sass, bison,
flex or all the COBOL preparsers tools).
"""
import logging
import mimetypes
import os
import re
import tempfile

from hackedit.api import utils
from hackedit.app import settings


def get_configs_for_mimetype(mimetype):
    """
    Gets all the possible pre-compiler configs for the given mimetype.

    I.e. get all gcc configs, all GnuCOBOL configs,...
    """
    from hackedit.api import plugins

    def get_user_configs_for_type_name(type_name):
        ret_val = []
        for config in settings.load_pre_compiler_configurations().values():
            if config.type_name == type_name:
                ret_val.append(config)
        return ret_val

    ret_val = []
    typenames = []
    # gets the list of compiler type names that are available for the mimetype
    for plugin in plugins.get_pre_compiler_plugins():
        if mimetype in plugin.get_pre_compiler_mimetypes():
            typenames.append(plugin.get_pre_compiler_type_name())
    for type_name in typenames:
        ret_val += plugins.get_pre_compiler_plugin_by_typename(type_name).get_auto_detected_configs()
        ret_val += get_user_configs_for_type_name(type_name)

    return ret_val


def _logger():
    return logging.getLogger(__name__)
