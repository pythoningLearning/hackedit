"""
The hackable editor for the desktop, built with Python3 and PyQt5.
"""
import os
import sys

if os.environ.get('HACKEDIT_DEV_MODE') is None:
    os.environ['QT_API'] = 'pyqt5'
    vendor = os.path.join(os.path.dirname(__file__), 'vendor')
    os.environ['HACKEDIT_VENDOR_PATH'] = vendor
    sys.path.insert(0, vendor)
    os.environ['PATH'] = vendor + os.pathsep + os.environ['PATH']


__version__ = '1.0a3.dev46'
