"""
This script compiles the ui files into python scripts.

YOU SHOULD START THIS SCRIPT FROM THE ROOT DIR OF THE SOURCE REPO:

python3 scripts/build_ui.py
"""
import os
import sys

print('Compiling *.ui files to python scripts...')

os.system(' '.join([sys.executable, 'setup.py', 'build_ui']))
