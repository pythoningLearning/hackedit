"""
This script run our test suite.

YOU SHOULD START THIS SCRIPT FROM THE ROOT DIR OF THE SOURCE REPO:

python3 scripts/tests/runtests.py
"""
import os
import sys

if 'tests' in os.getcwd():
    os.chdir('../..')

os.environ['PYTEST_QT_API'] = 'pyqt5'

os.system('%s setup.py  test' % sys.executable)
