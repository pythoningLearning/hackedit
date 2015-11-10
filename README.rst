.. image:: https://raw.githubusercontent.com/HackEdit/hackedit/master/docs/_static/banner.png

|

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/HackEdit/hackedit
   :target: https://gitter.im/HackEdit/hackedit?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

|

- `About`_
- `Status`_
- `Resources`_
- `License`_
- `Features`_
- `Dependencies`_
- `Plugins`_
- `Installation`_

  * `GNU/Linux`_
  * `Windows`_
  * `OS X`_

.. _About: https://github.com/HackEdit/hackedit#about
.. _Status: https://github.com/HackEdit/hackedit#status
.. _Resources: https://github.com/HackEdit/hackedit#resources
.. _Features: https://github.com/HackEdit/hackedit#features
.. _License: https://github.com/HackEdit/hackedit#license
.. _Installation: https://github.com/HackEdit/hackedit#installation
.. _GNU/Linux: https://github.com/HackEdit/hackedit#linux
.. _Windows: https://github.com/HackEdit/hackedit#windows
.. _OS X: https://github.com/HackEdit/hackedit#osx
.. _Plugins: https://github.com/HackEdit/hackedit#plugins

About
=====

The hackable IDE, built with `Python3`_, `PyQt5`_ and `pyQode`_.

HackEdit is an open platform to build an Integrated Development Environment.

This repository contains the core application which setups a basic IDE with a
plugin infrastructure and an API that you can use to enhance the application
and make it a full stack IDE for a particular technology.

The name stands from *Hackable Editor*, but there is another meaning: once
you've contributed to the project or made your own plugin, you can say that
you've *hacked it*.

**Note that the core application is actually pretty dumb, you need to install
some** `Plugins`_ **to make something out of HackEdit!**

Status
======

HackEdit is in **ALPHA**. Expects to find bugs and features not implemented.

At the moment there is **no user manual**, **no documentation**,
**no Windows installer**, **no linux packages**.

All those will come with future releases.

The **API** is **not** considered **stable** and we don't recommend to hack in
HackEdit. It's probably better to wait for the beta release, at that point,
there will be more resources available.

For now, just give it a try and **report** any issue you encountered, give your
**feedback** and submit any **idea** that you have.

You can discuss about HackEdit on `Gitter`_.

.. _Gitter: https://gitter.im/HackEdit/hackedit

Resources
=========

- `Homepage`_
- `Issue tracker`_
- `Changelog`_
- `Roadmap`_
- `Screenshots`_

.. _Homepage: https://github.com/HackEdit/hackedit
.. _Issue tracker: https://github.com/HackEdit/hackedit/issues
.. _Changelog: https://github.com/HackEdit/hackedit/blob/master/docs/changelog.rst
.. _Roadmap: https://github.com/HackEdit/hackedit/wiki/Roadmap
.. _Screenshots: https://github.com/HackEdit/hackedit/wiki/Screenshots

License
=======

HackEdit is released under the GPL version 2.

We are using the `Hack`_ font which is licensed under the Hack Open Font
License v2.0 and the Bitstream Vera License and the `Breeze`_ icon theme,
licensed under the LGPL.

Features
========

The core application provides the following features:

- cross platform: works on Linux, OS X and Windows
- coded in 100% pure Python, using the PyQt GUI toolkit
- plugin architecture with customisable workspaces: you can choose exactly what
  plugins to use for a specific project
- multi-window IDE with multiple undo stack
- splittable editor tabs
- supports multiple programming languages through plugins (at the momement we
  have support for Python and COBOL)
- configurable interface (custom shortcuts, native theme or dark theme,...)
- a clean and simple high level API for interacting with the IDE
- core plugins included: find/search in directories, editor outline view,
  simple terminal widget for running commands, open documents view,
  image viewer


Dependencies
============

**Main dependencies**:

- `Python3`_ (>= 3.4)
- `PyQt5`_
- `setuptools`_ and `pip`_ (might be included with your python installation).
- `git`_

**Optional dependencies**:

- `dill`_   (improved pickle)
- `pyyaml`_ (if your templates use boss.yml instead of boss.json)
- `PyGObject`_ and `libnotify`_ on GNU/Linux for nicer notifications on gtk based desktops.


The following dependencies are include in a zip archive and do not need to
be installed by the user.

- `pyqode.qt`_
- `pyqode.core`_
- `pyqode.cobol`_
- `pyqode.python`_
- `pygments`_
- `future`_
- `pep8`_
- `pyflakes`_
- `jedi`_
- `boss`_
- `cement`_
- `qdarkstyle`_

Plugins
=======

Plugins are regular python packages that install one or more setuptools entry-points.

You can install plugins for HackEdit either by using the builtin plugin manager
interface or by using the python package manager: `pip`_.

Here is the list of official plugins (made by the core team):

- `hackedit-python`_: Python support (python2 and python3 are supported)
- `hackedit-cobol`_: COBOL support

*Note: the plugin manager interface has not been implemented yet, you need to use pip to install the plugins*

Here is how you can install the official plugins::

    pip3 install hackedit-python hackedit-cobol


Installation
============

General instructions:
---------------------


1. install the following dependencies using your favorite package manager:

- Python 3
- pip (the python package manager) for Python3
- PyQt5 for python3  .


2. use pip to install ``hackedit`` and its python dependencies::

      pip3 install hackedit --upgrade


   To install the latest development version, run the following command instead::

      pip3 install git+https://github.com/HackEdit/HackEdit.git --upgrade

Once you've installed the core application, you will want to install some
`Plugins`_.

Linux
-----

Ubuntu/Debian
~~~~~~~~~~~~~

1. Install pip, setuptools and pyqt5::

    sudo apt-get install python3-setuptools python3-pip python3-pyqt5 python3-pyqt5.qtsvg git

2. Install optional dependencies (for nicer notifications on Gnome Shell 3.x/Unity)::

    sudo apt-get install python3-gi libnotify-dev

3. Install hackedit::

    sudo pip3 install hackedit --upgrade --install-option="--install-layout=deb"

4. If you're using a gtk based desktop, update the gtk icon cache::

    sudo gtk-update-icon-cache /usr/share/icons/hicolor/

5. Run hackedit::

    hackedit


ArchLinux
~~~~~~~~~

1. Install pip, setuptools and pyqt5 using pacman::

    sudo pacman -S python-pyqt5 python-pip python-setuptools qt5-svg git

2. Install optional dependencies (for nicer notification on Gnome Shell 3.x)::

    sudo pacman -S libnotify python-gobject

3. Install hackedit::

    sudo pip3 install hackedit --upgrade

4. If you're using a gtk based desktop, update the gtk icon cache::

    sudo gtk-update-icon-cache /usr/share/icons/hicolor/

5. Run hackedit::

    hackedit

Windows
-------

1. Install `Python 3.4`_

2. Install `PyQt5 for Python 3.4`_

3. Install `Git for Windows`_ and make sure it is added to PATH (if not the
templates repository won't get sync. Note that you can choose to not add it
to your system path but only in HackEdit *(Preferences->Environment->Environment Variables)*)

4. Open a command line prompt and run the following commands:

* Install hackedit using pip::

    pip install hackedit --upgrade

* Run hackedit in GUI mode::

    hackedit

* Or, run hackedit in console mode::

    hackedit-console

*Note: In the future, there will be a windows installer with a native launcher that your can pin to you taskbar.*


OSX
---

1. Install `Homebrew`_

2. Install Python3 and PyQt5 using::

    brew install pyqt5 --with-python3

3. Install hackedit::

    pip3 install hackedit --upgrade

4. Run hackedit from the terminal::

    hackedit

*Note: in the future, you will have a native launcher that you can keep in your dock.*

.. links section:

.. _github: https://github.com/HackEdit/hackedit
.. _hackedit-cobol: https://github.com/HackEdit/hackedit-cobol
.. _hackedit-python: https://github.com/HackEdit/hackedit-python

.. _Homebrew: http://brew.sh/

.. _Python3: https://www.python.org/
.. _PyQt5: http://www.riverbankcomputing.com/software/pyqt/download5
.. _setuptools: https://pypi.python.org/pypi/setuptools
.. _pip: https://pypi.python.org/pypi/pip

.. _dill: https://pypi.python.org/pypi/dill
.. _pyyaml: https://pypi.python.org/pypi/pyyaml

.. _pyQode: https://github.com/pyQode/pyQode
.. _pyqode.qt: https://github.com/pyQode/pyqode.qt
.. _pyqode.core: https://github.com/pyQode/pyqode.core
.. _pyqode.python: https://github.com/pyQode/pyqode.python
.. _pyqode.cobol: https://github.com/pyQode/pyqode.cobol

.. _pygments: https://pypi.python.org/pypi/pygments
.. _future: https://pypi.python.org/pypi/future
.. _pep8: https://pypi.python.org/pypi/pep8
.. _pyflakes: https://pypi.python.org/pypi/pyflakes
.. _jedi: https://pypi.python.org/pypi/jedi
.. _boss: https://pypi.python.org/pypi/boss
.. _cement: https://pypi.python.org/pypi/cement
.. _qdarkstyle: https://pypi.python.org/pypi/cement
.. _git: https://git-scm.com/
.. _Python 3.4: https://www.python.org/ftp/python/3.4.3/python-3.4.3.msi
.. _PyQt5 for Python 3.4: http://downloads.sourceforge.net/project/pyqt/PyQt5/PyQt-5.5.1/PyQt5-5.5.1-gpl-Py3.4-Qt5.5.1-x32.exe?r=&ts=1446908240&use_mirror=heanet
.. _Git for Windows: https://git-scm.com/download/win
.. _PyGObject: https://wiki.gnome.org/Projects/PyGObject
.. _libnotify: http://www.linuxfromscratch.org/blfs/view/svn/x/libnotify.html

.. _Hack: https://github.com/chrissimpkins/Hack
.. _Breeze: https://github.com/NitruxSA/breeze-icon-theme
