"""
A set of utility functions that plugin would use.
"""
import functools
import sys
import locale
import copy
import json
import os
from fnmatch import fnmatch

from PyQt5 import QtCore, QtWidgets

from hackedit.app import settings, mime_types


class block_signals:
    """
    Context manager that calls blockSignals on the QObject passed in
    parameters.

    Usage::

        with block_signals(qobject):
            pass  # do some stuff

    This is equivalent to::

        qobject.blockSignals(True)
        pass  # do some stuff
        qobject.blockSignals(False)

    """
    def __init__(self, qobject):
        self.qobject = qobject

    def __enter__(self):
        self.qobject.blockSignals(True)

    def __exit__(self, *args, **kwargs):
        self.qobject.blockSignals(False)


def add_environment_var_to_table(table):
    assert isinstance(table, QtWidgets.QTableWidget)
    key, ok = QtWidgets.QInputDialog.getText(table, "Add environment variable", "Key:")
    if not ok:
        return
    value, ok = QtWidgets.QInputDialog.getText(table, "Add environment variable", "Value:")
    if not ok:
        return
    index = table.rowCount()
    table.insertRow(index)
    key_item = QtWidgets.QTableWidgetItem()
    key_item.setText(key)
    value_item = QtWidgets.QTableWidgetItem()
    value_item.setText(value)
    table.setItem(index, 0, key_item)
    table.setItem(index, 1, value_item)
    table.selectRow(index)


def remove_selected_environment_var_from_table(table):
    assert isinstance(table, QtWidgets.QTableWidget)
    row = table.currentRow()
    if row == -1:
        return
    table.removeRow(row)
    row -= 1
    if row != -1:
        table.selectRow(row)
