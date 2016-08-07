"""
This script compiles hackedit.qrc file into a python script

YOU SHOULD START THIS SCRIPT FROM THE ROOT DIR OF THE SOURCE REPO:

python3 scripts/build_rc.py
"""
import os


print('Compiling hackedit.qrc to a python script...')

os.system(' '.join(['pyrcc5', 'data/resources/hackedit.qrc', '-o', 'hackedit/presentation/forms/hackedit_rc.py']))
