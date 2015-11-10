#!/usr/bin/env python3
"""
Startup script for hackedit developers, assuming all dependencies have been
installed to the python site-packages (you can install all dev dependencies by
running pip3 install -r requirements-dev.txt).

Note: if you would like to work on some pyqode packages, it is recommended to
install all pyqode packages as editable packages before running
``pip3 install -r requirements-dev`` (and make sure to install them in the
proper order: first pyqode.qt then pyqode.core. Afterwards the order does not matter.)


YOU SHOULD START THIS SCRIPT FROM THE ROOT DIR OF THE SOURCE REPO:

python3 scripts/hackedit-dev.py

"""
from hackedit.main import main


if __name__ == '__main__':
    main()
