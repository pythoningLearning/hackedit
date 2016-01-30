"""
Provides a series of function on top of gettext to retrieve a particular
translations (used by both the core apps and the plugins).
"""
import re
import gettext
import os
import sys

from PyQt5 import QtCore


def current_locale():
    """
    Gets the current locale defined in the application settings
    """
    default = 'fr'
    return QtCore.QSettings().value('env/locale', default)


def translation(package='hackedit'):
    """
    Gets the translation function for the language selected by the user.

    Use this function at the top of each of your plugin modules::

        from hackedit.api.gettext import translation
        _ = translation(package='hackedit-python')
        _('translatable string')

    :param package: Name of the package to get the translation for...

    :returns: None if package == 'hackedit' otherwise return the translation
              function usable directly in your module.
    """
    locale_dir = os.path.join(sys.prefix, 'share', 'locale')
    try:
        t = gettext.translation(package, localedir=locale_dir,
                                languages=[current_locale()])
        if package == 'hackedit':
            # we can install globally
            t.install()
            return t.gettext
        else:
            return t.gettext
    except OSError:
        return gettext.NullTranslations().gettext


def hackedit_gettext_hook(ui_script_path):
    """
    pyqt-distutils hook that will replace Qt translate tools by calls to
    ``hackedit.api.gettext.translation``.
    """
    from pyqt_distutils.config import Config

    with open(ui_script_path, 'r') as fin:
        content = fin.read()

    # replace ``_translate("context", `` by ``_(``
    content = re.sub(r'_translate\(".*",\s', '_(', content)

    # inject the _ function
    cfg = Config()
    cfg.load()
    package_name = cfg.package_name
    content = content.replace(
        '        _translate = QtCore.QCoreApplication.translate',
        '        from hackedit.api.gettext import translation\n'
        '        _ = translation(package="%s")' % package_name)

    with open(ui_script_path, 'w') as fout:
        fout.write(content)
