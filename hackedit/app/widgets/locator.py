import logging
import os
import re

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqode.core.api import DelayJobRunner, TextHelper, utils

from hackedit.api import editor, index, project, widgets
from hackedit.app.forms import locator_ui
from hackedit.app.index.db import get_search_tokens, DbHelper
from hackedit.app.widgets.html_delegate import HTMLDelegate


LIMIT = 50  # 50 items max


class LocatorWidget(QtWidgets.QFrame):
    """
    Popup widget that let the user quickly locate a file in a project.

    The user can also locate a symbol in the current editor with the ``@``
    operator or a symbol in the whole project with the ``#`` operator.

    The ``:`` operator can be used to specify the line number to go to.

    Note that all those operators are exclusive, you cannot mix
    ``@`` with ``:`` or with ``#``.
    """
    activated = QtCore.pyqtSignal(str, int)
    cancelled = QtCore.pyqtSignal()

    GOTO_LINE_PATTERN = re.compile(r'^.*:.*')
    GOTO_SYMBOL_PATTERN = re.compile('^@.*')
    GOTO_SYMBOL_IN_PROJ_PATTERN = re.compile('^!.*')

    MODE_GOTO_ANYTHING = 0
    MODE_GOTO_SYMBOL = 1
    MODE_GOTO_SYMBOL_IN_PROJECT = 2
    MODE_GOTO_LINE = 3

    def __init__(self, window=None):
        super().__init__()
        self.icon_provider = widgets.FileIconProvider()
        self._runner = DelayJobRunner(delay=100)
        self.main_window = window
        self.ui = locator_ui.Ui_Frame()
        self.ui.setupUi(self)
        self.ui.lineEdit.textChanged.connect(self.request_search)
        self.ui.lineEdit.prompt_text = _('Type to locate...')
        self.ui.lineEdit.installEventFilter(self)
        self.ui.treeWidget.installEventFilter(self)
        self.ui.treeWidget.setItemDelegate(HTMLDelegate())
        self.setWindowFlags(QtCore.Qt.Popup)
        self.ui.lineEdit.setFocus(True)
        self.ui.bt_close.clicked.connect(self.hide)
        self.ui.bt_infos.clicked.connect(self._show_help)
        self.mode = self.MODE_GOTO_ANYTHING
        self.ui.treeWidget.currentItemChanged.connect(
            self._on_current_item_changed)
        self.ui.treeWidget.itemDoubleClicked.connect(self._activate)
        self.ui.cb_non_project_files.toggled.connect(self._search)

    def showEvent(self, ev):
        self._activated = False
        self.ui.lineEdit.clear()
        if self.mode == self.MODE_GOTO_ANYTHING:
            self.search_files()
            self.ui.cb_non_project_files.setVisible(True)
        elif self.mode == self.MODE_GOTO_SYMBOL:
            self.ui.lineEdit.setText('@')
            self.search_symbol()
            self.ui.cb_non_project_files.setVisible(False)
        elif self.mode == self.MODE_GOTO_SYMBOL_IN_PROJECT:
            self.ui.lineEdit.setText('!')
            self.search_symbol_in_project()
            self.ui.cb_non_project_files.setVisible(True)
        elif self.mode == self.MODE_GOTO_LINE:
            self.ui.lineEdit.setText(':')
            self.ui.treeWidget.hide()
            self.adjustSize()
            self.ui.cb_non_project_files.setVisible(False)
        self.ui.lineEdit.setFocus()
        super().showEvent(ev)

    def closeEvent(self, ev):
        if not self._activated:
            self.cancelled.emit()
        super().closeEvent(ev)

    def eventFilter(self, obj, ev):
        if obj == self.ui.lineEdit and ev.type() == QtCore.QEvent.KeyPress:
            if ev.key() == QtCore.Qt.Key_Down:
                next_item = self.ui.treeWidget.itemBelow(
                    self.ui.treeWidget.currentItem())
                if next_item is None:
                    next_item = self.ui.treeWidget.topLevelItem(0)
                self.ui.treeWidget.setCurrentItem(next_item)
                return True
            elif ev.key() == QtCore.Qt.Key_Up:
                next_item = self.ui.treeWidget.itemAbove(
                    self.ui.treeWidget.currentItem())
                if next_item is None:
                    next_item = self.ui.treeWidget.topLevelItem(
                        self.ui.treeWidget.topLevelItemCount() - 1)
                self.ui.treeWidget.setCurrentItem(next_item)
                return True
            if ev.key() in [QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter] and ev.modifiers() & QtCore.Qt.ShiftModifier:
                self.ui.cb_non_project_files.setChecked(not self.ui.cb_non_project_files.isChecked())
                self.ui.lineEdit.setFocus(True)
                return True
            elif ev.key() in [QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter]:
                self._activate()
                return True
            if ev.key() in [QtCore.Qt.Key_Tab, QtCore.Qt.Key_Backtab]:
                # tab should not have any effect
                return True
        elif obj == self.ui.treeWidget and ev.type() == QtCore.QEvent.KeyPress\
                and ev.key() in [QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter]:
            self._activate()
            return True
        return super().eventFilter(obj, ev)

    def _activate(self, *_):
        if self.ui.treeWidget.isVisible():
            data = self.ui.treeWidget.currentItem().data(
                0, QtCore.Qt.UserRole)
        else:
            data = self.main_window.current_tab.file.path
        if isinstance(data, str):
            text = self.ui.lineEdit.text()
            if self.GOTO_LINE_PATTERN.match(text):
                line = self._get_requested_line_nbr()
            else:
                line = -1
            self.activated.emit(data, line)
        elif isinstance(data, tuple):
            line, path = data
            self.activated.emit(path, line)
        self._activated = True
        self.close()

    def request_search(self):
        self._runner.request_job(self._search)

    def _search(self):
        text = self.ui.lineEdit.text()
        # check the source to use for search (symbols or files).
        if self.GOTO_SYMBOL_PATTERN.match(text):
            self.ui.cb_non_project_files.setVisible(False)
            if self.GOTO_LINE_PATTERN.match(text):
                self.ui.treeWidget.hide()
                self.adjustSize()
            elif editor.get_current_editor():
                self.search_symbol()
        elif self.GOTO_SYMBOL_IN_PROJ_PATTERN.match(text):
            if self.GOTO_LINE_PATTERN.match(text):
                self.ui.cb_non_project_files.setVisible(False)
                self.ui.treeWidget.hide()
                self.adjustSize()
            else:
                self.ui.cb_non_project_files.setVisible(True)
                self.search_symbol_in_project()
        else:
            if not text.startswith(':'):
                self.ui.cb_non_project_files.setVisible(True)
                self.search_files()
            else:
                self.ui.cb_non_project_files.setVisible(False)
                # will be used to goto line in the current editor.
                self.ui.treeWidget.hide()
                self.adjustSize()
                e = editor.get_current_editor()
                try:
                    TextHelper(e).goto_line(self._get_requested_line_nbr() - 1)
                except (ValueError, AttributeError):
                    _logger().debug('failed to go to line on editor %r', e)

    def _get_projects(self):
        if self.ui.cb_non_project_files.isChecked():
            return None
        # all active project
        return project.get_projects()

    def search_symbol(self):
        search_term = self._get_search_term()
        fpath = editor.get_current_editor().file.path
        symbols = index.get_symbols(name_filter=search_term, file=fpath)

        # display
        self.ui.treeWidget.clear()
        first_item = None
        for i, (symbol_item, file_item) in enumerate(symbols):
            name = symbol_item.name
            line = symbol_item.line + 1
            path = file_item.path
            text = '%s<br><i>%s:%d</i>' % (self.get_enriched_text(name, search_term), path, line)

            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, text)
            item.setIcon(0, self.icon_provider.icon(path))
            item.setData(0, QtCore.Qt.UserRole, (line, path))
            if first_item is None:
                first_item = item
            self.ui.treeWidget.addTopLevelItem(item)
            if i > LIMIT:
                break
        if self.ui.treeWidget.topLevelItemCount():
            self.ui.treeWidget.show()
            self.ui.treeWidget.setCurrentItem(first_item)
        else:
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, _('No match found'))
            item.setIcon(0, QtGui.QIcon.fromTheme('dialog-warning'))
            self.ui.treeWidget.addTopLevelItem(item)
        self.adjustSize()

    def search_symbol_in_project(self):
        search_term = self._get_search_term()
        symbols = index.get_symbols(name_filter=search_term, projects=self._get_projects())

        # display
        self.ui.treeWidget.clear()
        first_item = None
        for i, (symbol_item, file_item) in enumerate(symbols):
            name = symbol_item.name
            line = symbol_item.line + 1
            path = file_item.path
            text = '%s<br><i>%s:%d</i>' % (self.get_enriched_text(name, search_term), path, line)
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, text)
            item.setIcon(0, self.icon_provider.icon(path))
            item.setData(0, QtCore.Qt.UserRole, (line, path))
            if first_item is None:
                first_item = item
            self.ui.treeWidget.addTopLevelItem(item)
            if i > LIMIT:
                break
        if self.ui.treeWidget.topLevelItemCount():
            self.ui.treeWidget.show()
            self.ui.treeWidget.setCurrentItem(first_item)
        else:
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, _('No match found'))
            item.setIcon(0, QtGui.QIcon.fromTheme('dialog-warning'))
            self.ui.treeWidget.addTopLevelItem(item)
        self.adjustSize()

    def get_definition_icon(self, icon):
        if isinstance(icon, list):
            icon = tuple(icon)
        return self._get_definition_icon(icon)

    @utils.memoized
    @staticmethod
    def _get_definition_icon(icon):
        if isinstance(icon, tuple):
            icon = QtGui.QIcon.fromTheme(
                icon[0], QtGui.QIcon(icon[1]))
        elif isinstance(icon, str):
            if QtGui.QIcon.hasThemeIcon(icon):
                icon = QtGui.QIcon.fromTheme(icon)
            else:
                icon = QtGui.QIcon(icon)
        return icon

    def search_files(self):
        name_filter = self._get_search_term()
        # get files from db
        project_files = index.get_files(name_filter=name_filter, projects=self._get_projects())

        # display
        self.ui.treeWidget.clear()
        first_item = None
        for i, file_item in enumerate(project_files):
            path = file_item.path
            name = file_item.name
            text = '%s<br><i>%s</i>' % (self.get_enriched_text(name, name_filter), os.path.dirname(path))
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, text)
            item.setIcon(0, self.icon_provider.icon(path))
            item.setData(0, QtCore.Qt.UserRole, path)
            if first_item is None:
                first_item = item
            self.ui.treeWidget.addTopLevelItem(item)
            if i > LIMIT:
                break
        if self.ui.treeWidget.topLevelItemCount():
            self.ui.treeWidget.show()
            self.ui.treeWidget.setCurrentItem(first_item)
        else:
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, _('No match found'))
            item.setIcon(0, QtGui.QIcon.fromTheme('dialog-information'))
            self.ui.treeWidget.addTopLevelItem(item)
        self.adjustSize()

    @staticmethod
    def get_match_spans(expr, item):
        spans = []
        item = item.lower()
        search_expr = DbHelper._get_searchable_name(expr)
        for token in get_search_tokens(search_expr):
            if not token:
                continue
            try:
                start = item.index(token)
                length = len(token)
                spans.append((start, length))
                to_replace = item[start:length]
                item = item.replace(to_replace, len(to_replace) * '*')
            except ValueError:
                pass
        return spans

    @staticmethod
    def get_enriched_text(item, expr):
        spans = LocatorWidget.get_match_spans(expr, item)
        offset = 0
        enriched = ''
        for start, end in sorted(spans, key=lambda x: x[0]):
            enriched += item[offset:start] + '<b>' + item[start:start + end] + '</b>'
            offset = start + end
        enriched += item[offset:]
        return enriched

    def _get_search_term(self):
        text = self.ui.lineEdit.text()
        if text.startswith('@'):
            text = text[1:]
        elif text.startswith('!'):
            text = text[1:]
        if self.GOTO_LINE_PATTERN.match(text):
            text = text.split(':')[0]
        return text.strip().replace("'", '').replace('"', '').replace('*', '')

    def _get_requested_line_nbr(self):
        text = self.ui.lineEdit.text()
        try:
            return int(text.split(':')[1])
        except (IndexError, ValueError):
            return -1

    def _show_help(self):
        help_text = _('''<p>Use <i>Goto</i> to navigate your project’s files
swiftly.</p>

<p>Use the <i>arrow keys</i> to navigate into the list and press <i>ENTER</i>
to open the selected entry. Press <i>ESCAPE</i> to close the popup window.<p>

<p><i>Goto</i> accepts several operators:

<ul>
    <li> <b>@</b> to locate a symbol in the current editor.</li>
    <li> <b>!</b> to locate a symbol in the opened project(s).</li>
    <li> <b>:</b> to specify the line number to go to.</li>
</ul>

</p>
''')
        QtWidgets.QMessageBox.information(
            self, _('Goto: help'), help_text)
        self.show()

    def _on_current_item_changed(self, item):
        text = self.ui.lineEdit.text()
        if item and self.GOTO_SYMBOL_PATTERN.match(text):
            line, path = item.data(0, QtCore.Qt.UserRole)
            TextHelper(editor.get_current_editor()).goto_line(line - 1)


# The following 3 functions have been taken from SpyderIDE.
NOT_FOUND_SCORE = -1
NO_SCORE = 0


def _logger():
    return logging.getLogger(__name__)


if __name__ == '__main__':
    print(LocatorWidget.get_enriched_text('test_my_editor', 'test'))
    print(LocatorWidget.get_enriched_text('test_my_editor', 'test edit'))
    print(LocatorWidget.get_enriched_text('test_my_editor', 'test editor'))
    print(LocatorWidget.get_enriched_text('test_my_editor', 'editor test'))
    print(LocatorWidget.get_enriched_text('code_edit', 'code_e'))