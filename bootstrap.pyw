#!/usr/bin/env python3
"""
The bootstrap script lets you run HackEdit from source checkout:

1) patch sys.path with the extlibs archive that contains most external
   libraries


Before running this script, you should:

1) install python3 and pyqt5 using your package manager (or the installer
   files for your platform)

2) install hackedit as an editable package::

       (sudo) pip3 install -e

   This is needed so that the plugin entrypoints are written to
   hackedit.egg-info/

3) install additional plugins (e.g. hackedit-cobol, hackedit-python) as
   editable packages (pip3 install -e .)

4) run the script: python3 bootstrap.pyw

"""
import glob
import logging
import os
import os.path as osp
import sys


logger = logging.getLogger('boostrap')
sh = logging.StreamHandler()
formatter = logging.Formatter(
    fmt='%(asctime)s.%(msecs)03d::%(levelname)s::%(name)s::%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
sh.setFormatter(formatter)
logger.addHandler(sh)
logger.setLevel(logging.INFO)


# --------- bootstrapping HackEdit
logger.info("Executing HackEdit from source checkout")

# ------ patching sys.path
DEVPATH = osp.dirname(osp.abspath(__file__))
sys.path.insert(0, DEVPATH)
ZIP_PATH = osp.normpath(osp.join(DEVPATH, 'data/share/extlibs.zip'))
os.environ['HACKEDIT_LIBS_PATH'] = ZIP_PATH
sys.path.insert(0, ZIP_PATH)

logger.info("01. Patched sys.path with %r", [DEVPATH, ZIP_PATH])

# ------ check if python setup.py develop has been executed
if len(glob.glob('*.egg-info')) == 0:
    logger.warning('Please run ``(sudo) pip3 install -e .`` to install '
                   'all dependencies and plugins...')

# ------ check PyQt5
try:
    from PyQt5.QtCore import PYQT_VERSION_STR
    from PyQt5.QtCore import QT_VERSION_STR
    from PyQt5.QtGui import QIcon
except ImportError:
    logger.exception('02. Failed to import PyQt5, package not found.')
    sys.exit(1)
else:
    logger.info('02. Imported PyQt5')
    logger.info('    [Qt %s, PyQt5 %s]' % (QT_VERSION_STR, PYQT_VERSION_STR))
    if 'linux' not in sys.platform.lower():
        paths = QIcon.themeSearchPaths()
        paths.append('data/resources/icons')
        QIcon.setThemeSearchPaths(paths)


# ------ run the application
try:
    from hackedit.main import main
    from hackedit.app import versions
except ImportError:
    logger.exception('03. Failed to import hackedit')
else:
    all_versions = versions.get_versions()
    logger.info("03. Imported HackEdit %s (%s)" % (
        all_versions['hackedit'], versions.get_vcs_revision()))
    logger.info("    [Python %s %dbits, on %s]" % (
        all_versions['python'], all_versions['bitness'],
        all_versions['system']))
    main()
