"""
This module contains a plugin that show a terminal in the bottom
area of the window.
"""
import logging
import os
import shlex

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqode.core.api import ColorScheme

from hackedit import api
from hackedit.app.forms import terminal_widget_ui, dlg_terminal_history_ui


def _logger():
    return logging.getLogger(__name__)


class Terminal(api.plugins.WorkspacePlugin):
    """
    Adds a terminal widget that let your run commands from within the IDE.
    """
    def activate(self):
        self.widget = _Terminal(api.window.get_main_window())
        self.widget.apply_preferences()
        dock = api.window.add_dock_widget(
            self.widget, _('Terminal'), QtGui.QIcon.fromTheme(
                'utilities-terminal'),
            QtCore.Qt.BottomDockWidgetArea)
        dock.hide()
        dock.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Expanding)

    def close(self):
        self.widget.close()

    def apply_preferences(self):
        self.widget.apply_preferences()


def _unique(seq):
    if seq:
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x)) and x]
    return ['']


class _Terminal(QtWidgets.QWidget):
    """
    Combines a line edit and an interactive console to simulate a terminal.

    You type your command in the line edit and see its execution in the
    interactive console.

    Features:
        - history + completer
        - Ctrl+L to clear the terminal
        - Ctrl+C to kill the process
        - current working dir based on the current project path
    """
    def __init__(self, window):
        super().__init__()
        window.current_project_changed.connect(
            self._on_current_project_changed)
        self._history = _unique(QtCore.QSettings().value(
            '_cache/terminal_history', []))
        self._history_index = -1
        self.main_window = window
        self._ui = terminal_widget_ui.Ui_Form()
        self._ui.setupUi(self)
        self._completer = QtWidgets.QCompleter(self._ui.edit_command)
        self._update_model()
        self._ui.edit_command.setCompleter(self._completer)
        self._ui.edit_command.button.setIcon(QtGui.QIcon.fromTheme(
            'edit-clear'))
        self._ui.edit_command.prompt_text = _('Type a command here')
        self._ui.bt_run.clicked.connect(self._run)
        self._ui.bt_run.setIcon(QtGui.QIcon.fromTheme('system-run'))
        self._ui.edit_command.returnPressed.connect(self._run)
        self._ui.edit_command.installEventFilter(self)
        self._ui.console.installEventFilter(self)
        self._ui.console.process_finished.connect(self._on_process_finished)
        self._cwd = self.main_window.current_project

        self.action_edit_history = QtWidgets.QAction(
            _('Edit history'), self._ui.bt_run)
        self.action_edit_history.setToolTip(_('Edit history'))
        self.action_edit_history.triggered.connect(self._edit_history)
        self._ui.bt_run.addAction(self.action_edit_history)

        self.action_clear_history = QtWidgets.QAction(
            _('Clear history'), self._ui.bt_run)
        self.action_clear_history.setToolTip(_('Clear history'))
        self.action_clear_history.setIcon(QtGui.QIcon.fromTheme('edit-clear'))
        self.action_clear_history.triggered.connect(self._clear_history)
        self._ui.bt_run.addAction(self.action_clear_history)

    def close(self):
        self.main_window = None

    def apply_preferences(self):
        cs = api.utils.color_scheme()
        self._ui.console.apply_color_scheme(ColorScheme(cs))

    def _clear_history(self):
        QtCore.QSettings().setValue('_cache/terminal_history', [])
        self._history = _unique(QtCore.QSettings().value(
            '_cache/terminal_history', []))
        self._history_index = -1
        self._update_model()

    def _update_model(self):
        model = QtCore.QStringListModel()
        model.setStringList(self._history)
        self._completer.setModel(model)

    def showEvent(self, event):
        self._ui.edit_command.setFocus()
        super().showEvent(event)

    def _run(self):
        cmd = self._ui.edit_command.text().strip()
        if not cmd:
            _logger().debug('empty command, quitting')
            return
        if cmd.startswith('cd '):
            path = cmd.replace('cd ', '').strip()
            path = os.path.abspath(os.path.join(self._cwd, path))
            if not os.path.exists(path):
                self._ui.console.setText(
                    _('cd: The directory %r does not exist') % path)
            else:
                self._cwd = path
                self._ui.console.clear()
                self._ui.console.setText('cd: %s' % path)
            return
        _logger().debug('running command %r' % cmd)
        self._history.insert(0, cmd)
        self._history = _unique(self._history)
        self._update_model()
        self._save_history()
        tokens = shlex.split(cmd, posix=False)
        pgm = tokens[0]
        args = tokens[1:]
        if pgm.strip() == 'sudo' and args[0] != '-S':
            # to make sur works we need to tell it that the password
            # will come from stdin.
            _logger().debug('sudo command invoked without -S, adding -S '
                            'automatically...')
            args.insert(0, '-S')
        if pgm.strip() == 'sudo':
            self._ui.console.mask_user_input = True
        else:
            self._ui.console.mask_user_input = False
        self._ui.console.clear()
        self._ui.console.stop_process()
        self._ui.console.start_process(pgm, args=args, cwd=self._cwd)
        self._ui.console.setFocus()
        self._last_command = ' '.join([pgm] + args)

    def _save_history(self):
        QtCore.QSettings().setValue('_cache/terminal_history', self._history)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.modifiers() & QtCore.Qt.ControlModifier:
                if event.key() == QtCore.Qt.Key_L:
                    self._ui.console.clear()
                elif event.key() == QtCore.Qt.Key_C:
                    self._ui.console.stop_process()
            else:
                flg = False
                if event.key() == QtCore.Qt.Key_Up:
                    self._history_index += 1
                    flg = True
                elif event.key() == QtCore.Qt.Key_Down:
                    self._history_index -= 1
                    flg = True
                if flg:
                    if self._history_index < 0:
                        self._history_index = 0
                    elif self._history_index >= len(self._history):
                        self._history_index = len(self._history) - 1
                    _logger().debug('history index: %d', self._history_index)
                    _logger().debug('history: %r', self._history)
                    try:
                        history_item = self._history[self._history_index]
                        _logger().debug('showing history item: %r',
                                        history_item)
                        self._ui.edit_command.setText(history_item)
                    except IndexError:
                        _logger().exception('failed to find history item'
                                            '(index=%d, history=%r)',
                                            self._history_index, self._history)
        try:
            return super().eventFilter(obj, event)
        except RuntimeError:
            # wrapped C/C++ object of type _Terminal has been deleted
            return False

    def _on_current_project_changed(self, new_path):
        self._cwd = new_path

    def _on_process_finished(self):
        if self._ui.console.hasFocus():
            self._ui.edit_command.setFocus()
        if not self.isVisible() or QtWidgets.qApp.activeWindow() != \
                self.main_window:
            e = api.events.Event(
                _('Command finished'),
                _('The command %r finished with exit code %d') % (
                    self._last_command, self._ui.console.exit_code))
            api.events.post(e)

    def _edit_history(self):
        new_history = DlgTerminalHistory.edit_history(self, self._history)
        if new_history:
            self._history = new_history
            self._save_history()
            self._update_model()


class DlgTerminalHistory(QtWidgets.QDialog):
    def __init__(self, parent, history):
        def create_item(x):
            item = QtWidgets.QListWidgetItem(self.ui.listWidget)
            item.setText(x)
            item.setIcon(QtGui.QIcon.fromTheme('utilities-terminal'))
            self.ui.listWidget.addItem(item)

        super().__init__(parent)
        self.ui = dlg_terminal_history_ui.Ui_Dialog()
        self.ui.setupUi(self)
        for entry in history:
            create_item(entry)
        self.ui.listWidget.itemSelectionChanged.connect(self._update_bt_state)
        self.ui.bt_remove.clicked.connect(self._rm_entry)
        self._update_bt_state()

    def _update_bt_state(self):
        self.ui.bt_remove.setEnabled(
            len(self.ui.listWidget.selectedItems()) > 0)

    def _rm_entry(self):
        for item in self.ui.listWidget.selectedItems():
            self.ui.listWidget.takeItem(self.ui.listWidget.row(item))

    def get_history(self):
        return [self.ui.listWidget.item(i).text()
                for i in range(self.ui.listWidget.count())]

    @staticmethod
    def edit_history(parent, history):
        dlg = DlgTerminalHistory(parent, history)
        if dlg.exec_() == dlg.Accepted:
            return dlg.get_history()
        return None
