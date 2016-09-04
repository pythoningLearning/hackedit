import os

os.environ['PYTEST_QT_API'] = 'pyqt5'
os.environ['QT_API'] = 'pyqt5'
os.environ['HACKEDIT_CORE_TEST_SUITE'] = '1'


from hackedit import __version__
from hackedit.main.apps.gui import GuiApplication


class TestApplication(GuiApplication):
    ORG_NAME = 'HackEdit-Tests'
    ORG_DOMAIN = 'tests.hackedit.com'


print('HackEdit v%s' % __version__)
app = TestApplication()

if os.environ.get('TRAVIS', False):
    from PyQt5.QtGui import QIcon
    QIcon.setThemeName('gnome')
