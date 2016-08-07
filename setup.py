#!/usr/bin/env python3
"""
Setup script for HackEdit
"""
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import hackedit


# Define a test command that run our test suite using py.test
class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        super().initialize_options()
        self.pytest_args = []

    def finalize_options(self):
        super().finalize_options()

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


# Define a command for updating the compile ui/qrc files to python scripts
# Requires the pyqt-distutils package.
try:
    from pyqt_distutils.build_ui import build_ui
except ImportError:
    build_ui = None

# Babel commands for internationalisation and localisation
try:
    from babel.messages import frontend as babel
except ImportError:
    compile_catalog = None
    extract_messages = None
    init_catalog = None
    update_catalog = None
else:
    compile_catalog = babel.compile_catalog
    extract_messages = babel.extract_messages
    init_catalog = babel.init_catalog
    update_catalog = babel.update_catalog


# Get long description
with open('README.rst', 'r') as readme:
    long_desc = readme.read()


# Get data files
# zip contains 3rd party libraries
data_files = []
# translations
translations = [
    ('share/locale/%s' % x[0].replace('data/locale/', ''),
     list(map(lambda y: x[0]+'/'+y, x[2])))
    for x in os.walk('data/locale/')
]
for dst, srclist in translations:
    checked_srclist = []
    for src in srclist:
        if src.endswith('.mo'):
            checked_srclist.append(src)
    if checked_srclist:
        data_files.append((dst, checked_srclist))

# platform specific files
if 'linux' in sys.platform.lower():
    # install launcher on linux
    data_files += [
        ('share/applications', ['data/share/hackedit.desktop']),
        ('share/icons/hicolor/scalable/apps', ['data/resources/icons/hackedit.svg'])]
else:
    # distribute icon theme on OSX/Windows
    base = 'data/resources/icons/'
    for name in ['Breeze', 'Breeze Dark']:
        directory = base + name
        data_files += [
            ('share/hackedit/icons/%s' % x[0].replace('%s' % base, ''),
             list(map(lambda y: x[0]+'/'+y, x[2]))) for x in os.walk(directory)
        ]


if 'bdist_wheel' in sys.argv:
    raise RuntimeError("This setup.py does not support wheels")


console_wrapper_entrypoint = 'heconsole = hackedit.console:main'

# run setup
setup(
    name='hackedit',
    version=hackedit.__version__,
    packages=find_packages(exclude=['tests']),
    py_modules=['pytest_hackedit'],
    keywords=['IDE', 'Intergrated Development Environment', 'TextEditor',
              'Editor'],
    data_files=data_files,
    url='https://github.com/HackEdit/hackedit',
    license='GPL',
    author='Colin Duquesnoy',
    author_email='colin.duquesnoy@gmail.com',
    description='The hackable IDE, built with Python3, PyQt5 and pyQode',
    long_description=long_desc,
    test_suite="tests",
    tests_require=['pytest', 'pytest-qt', 'pytest-mock'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        # Main gui script
        'gui_scripts': ['hackedit = hackedit.main.main_gui:main'],
        'console_scripts': [
            'hackedit-console = hackedit.main.main_gui:main',
            console_wrapper_entrypoint] if sys.platform == 'win32' else [
            console_wrapper_entrypoint
        ],
        # Plugin entry-points
        'hackedit.main.plugins.editors': [
            'ImageViewer = hackedit.main.plugins.image_viewer:ImageViewer',
            'RstCodeEditPlugin = hackedit.main.plugins.editors:RstCodeEditPlugin',
            'JSONCodeEditPlugin = hackedit.main.plugins.editors:JSONCodeEditPlugin'
        ],
        'hackedit.main.plugins.file_icon_providers': [],
        'hackedit.main.plugins.workspace_plugins': [
            'Terminal = hackedit.main.plugins.terminal:Terminal',
            'FindReplace = hackedit.main.plugins.find_replace:FindReplace',
            'DocumentOutline = hackedit.main.plugins.outline:DocumentOutline',
            'OpenDocuments = hackedit.main.plugins.documents:OpenDocuments',
            'HtmlPreview = hackedit.main.plugins.html_preview:HtmlPreview'
        ],
        'hackedit.main.plugins.workspace_providers': [
            'generic_workspace = hackedit.main.plugins.workspaces:GenericWorkspace',
            'empty_workspace = hackedit.main.plugins.workspaces:EmptyWorkspace',
        ],
        'pygments.styles': [
            'aube = hackedit.presentation.styles.aube:AubeStyle',
            'crepuscule = hackedit.presentation.styles.crepuscule:CrepusculeStyle',
            'ark-dark = hackedit.presentation.styles.arkdark:ArkDarkStyle',
            'midna-dark = hackedit.presentation.styles.midnadark:MidnaDarkStyle',
        ],
        'pyqt_distutils_hooks': [
            'hackedit_gettext = hackedit.application.i18n:hackedit_gettext_hook']
    },
    cmdclass={
        'test': PyTest,
        'build_ui': build_ui,
        'compile_catalog': compile_catalog,
        'extract_messages': extract_messages,
        'init_catalog': init_catalog,
        'update_catalog': update_catalog
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications :: Qt',
        'Environment :: Win32 (MS Windows)',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
        'Topic :: Text Editors :: Integrated Development Environments (IDE)'
    ]
)
