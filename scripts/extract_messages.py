"""
This script compiles the ui files into python scripts.

YOU SHOULD START THIS SCRIPT FROM THE ROOT DIR OF THE SOURCE REPO:

python3 scripts/build_ui.py
"""
import subprocess
import sys

print('Extracting messages')

print(
    subprocess.check_output([
        sys.executable, 'setup.py', 'extract_messages',
        '--output-file', 'data/locale/messages.pot', '--verbose']).decode('utf-8'))
