import pytest
from PyQt5 import QtWidgets

from hackedit.api import utils
from hackedit.app import mime_types, settings


def test_add_mimetype_extension():
    settings.load()
    settings._SETTINGS.clear()
    mtype = 'text/x-own'
    ext = '.own'
    assert ext not in mime_types.get_extensions(mtype)
    utils.add_mimetype_extension(mtype, ext)
    assert ext in mime_types.get_extensions(mtype)


def test_get_mimetype_filter():
    ret = utils.get_mimetype_filter('text/x-python')
    assert 'text/x-python (*.py *.pyw ' in ret


def test_block_signal(qtbot):
    toggled = False
    def on_toggle():
        toggled = True

    checkbox = QtWidgets.QCheckBox()
    checkbox.toggled.connect(on_toggle)
    with utils.block_signals(checkbox):
        checkbox.toggle()
    assert toggled is False
    checkbox.toggle()
    assert toggled is True
