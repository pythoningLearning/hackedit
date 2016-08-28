import logging
import os
import shutil
import sys

from PyQt5 import QtWidgets
from hackedit import __version__
from hackedit.api.i18n import get_translation
from hackedit.containers import Services


class BaseApplication(QtWidgets.QApplication):
    ORG_NAME = 'HackEdit'
    ORG_DOMAIN = 'hackedit.com'

    def __init__(self):
        super().__init__(sys.argv)
        self._init_qt_app()
        self._init_sqlite3()
        get_translation()
        Services.logging().set_level(logging.DEBUG)
        Services.plugin_manager()

    def _init_qt_app(self):
        self.setOrganizationName(self.ORG_NAME)
        self.setOrganizationDomain(self.ORG_DOMAIN)
        self.setApplicationDisplayName(self.ORG_NAME)
        self.setApplicationName(self.ORG_NAME)
        self.setApplicationVersion(__version__)
        QtWidgets.qApp = self

    def _init_sqlite3(self):
        if sys.platform == 'win32':
            vendor = os.environ['HACKEDIT_VENDOR_PATH']
            # copy _sqlite3.pyd next to our own sqlite3.dll (with fts4 support enabled)
            pyd = os.path.join(os.path.dirname(sys.executable), 'DLLs', '_sqlite3.pyd')
            try:
                shutil.copy(pyd, vendor)
            except PermissionError:
                # already copied and in use
                pass
            # select the correct sqlite3 dll at runtime depending on the bitness of
            # the python intepreter, see github issue #75
            bitness = 64 if sys.maxsize > 2**32 else 32
            src_dll = os.path.join(vendor, 'sqlite3-%dbits.dll' % bitness)
            dst_dll = os.path.join(vendor, 'sqlite3.dll')
            try:
                shutil.copy(src_dll, dst_dll)
            except PermissionError:
                # already copied and in use
                pass
