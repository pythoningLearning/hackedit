"""
This module contains a small API built on top of the python mimetypes module
to manipulate user defined mimetypes.
"""
import json
import logging
import mimetypes

import pkg_resources
from dependency_injector.injections import inject
from hackedit.application import system
from hackedit.containers import Services
from pygments.lexers import get_all_lexers, get_lexer_for_mimetype
from pyqode.core.widgets import SplittableCodeEditTabWidget


# monkeypatch pygments.plugin.find_plugin_lexers
def find_plugin_lexers():  # pragma: no cover
    """
    Copy of pygments.plugins.find_plugin_lexers to avoid RequirementParseError
    (issue introduced in setuptools 20.2)
    """
    if pkg_resources is None:
        return
    for entrypoint in pkg_resources.iter_entry_points('pygments.lexers'):
        try:
            yield entrypoint._load()
        except pkg_resources.RequirementParseError:
            continue


from pygments import plugin  # noqa
plugin.find_plugin_lexers = find_plugin_lexers
# execute it once to make sure the cache is built using our monkeypatched
# function
list(plugin.find_plugin_lexers())


def _logger():
    return logging.getLogger(__name__)


class MimeTypesService:
    @inject(settings=Services.settings)
    def __init__(self, settings):
        self._settings = settings
        self._load()

    def get_supported_mimetypes(self):
        """
        Returns the list of supported mimetypes.

        This list is build up on the list of editor plugins and their supported
        mimetypes.
        """
        keys = SplittableCodeEditTabWidget.editors.keys()
        ret_val = []
        for k in keys:
            ret_val.append(k)
        # all other mimetypes are handled by the fallback editor
        for _, _, filenames, mtypes in get_all_lexers():
            if len(mtypes) and len(filenames):
                ret_val.append(mtypes[0])
        return list(set(ret_val))

    def get_handler(self, mimetype):
        """
        Get the handler (editor) for a given mimetype.
        """
        try:
            return SplittableCodeEditTabWidget.editors[mimetype]
        except KeyError:
            return SplittableCodeEditTabWidget.fallback_editor

    def get_extensions(self, mimetype):
        """
        Gets the list of extensions for a given mimetype. This function
        will return both the builtin extensions and the user defined extensions.
        """
        string = self._settings.environment.mimetypes
        db = json.loads(string)
        try:
            custom = db[mimetype]
        except KeyError:
            try:
                l = get_lexer_for_mimetype(mimetype)
            except Exception:
                custom = ['*%s' % ext for ext in
                          mimetypes.guess_all_extensions(mimetype)]
            else:
                custom = l.filenames
        return sorted([ext for ext in set(custom) if ext])

    def set_extensions(self, mimetype, extensions):
        """
        Sets the list of user defined extension for a given mimetype.

        This mapping is stored in QSettings. Use :func:`load` to apply the new
        types.

        :param mimetype: The mimetype to add. If the extension
        :param extension: the extension to map with mimetype.
        """
        string = self._settings.environment.mimetypes
        db = json.loads(string)
        db[mimetype] = sorted(extensions)
        self._settings.environment.mimetypes = json.dumps(db)
        for ext in extensions:
            mimetypes.add_type(mimetype, ext.replace('*', ''))

    def reset_custom_extensions(self):
        """
        Resets custom extensions, only builtins will be kept
        """
        self._settings.environment.mimetypes = '{}'
        self._load()

    def get_mimetype_filter(self, mtype):
        """
        Gets the open file dialog filter for a given mimetype.

        :param mtype: Mime type (e.g. 'text/x-python' or 'text/x-cobol').
        """
        exts = ' '.join(self.get_extensions(mtype))
        return '%s (%s)' % (mtype, exts)

    def add_mimetype_extension(self, mimetype, extension):
        """
        Adds an extension to an existing mimetype. If the mimetypes does not
        exists it is automatically added to the mimetypes database.

        :param mimetype: mimetype to modify
        :param extension: extension to add
        :return:
        """
        exts = self.get_extensions(mimetype)
        exts.append(extension)
        exts = list(set(exts))
        self.set_extensions(mimetype, exts)

    def remove_mimetype_extension(self, mimetype, extension):
        exts = self.get_extensions(mimetype)
        try:
            exts.remove(extension)
        except ValueError:
            return
        else:
            exts = list(set(exts))
            self.set_extensions(mimetype, exts)

    def _load(self):
        """
        Loads user defined mimetypes and extension into standard module.

        This function is called once on startup by the application and can be
        called later to update the mimetypes db.
        """
        string = self._settings.environment.mimetypes
        db = json.loads(string)
        if not db:
            _logger().debug('loading default mimetypes')
            db = self._get_default_mimetypes()
            _logger().debug('default mimetypes loaded')

        if not system.LINUX:
            for mimetype, exts in db.items():
                if not exts:
                    continue
                for ext in exts:
                    mimetypes.add_type(mimetype, ext.replace('*', ''))

    def _get_default_mimetypes(self):
        ret_val = {}
        if not system.LINUX:
            for mtype in self.get_supported_mimetypes():
                exts = self.get_extensions(mtype)
                ret_val[mtype] = exts
        return ret_val
