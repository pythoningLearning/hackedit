import os
import logging
from PyQt5 import QtWidgets

from hackedit import __version__
from hackedit.api import versions
from hackedit.app import logger, settings
from hackedit.app.forms import dlg_about_ui

FLG_SHOW_MSG_BOX = False


LEVELS_VALUES = {
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'PYQODE_DEBUG': 1,
}


LEVEL_NAMES = {v: k for k, v in LEVELS_VALUES.items()}


class DlgAbout(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = dlg_about_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.lbl_version.setText(self.ui.lbl_version.text() % __version__)

        # Load log file content
        try:
            with open(logger.get_path()) as f:
                log_content = f.read()
        except FileNotFoundError:
            log_content = ''
        self.ui.edit_log.setPlainText(log_content)
        tc = self.ui.edit_log.textCursor()
        tc.movePosition(tc.End)
        self.ui.edit_log.setTextCursor(tc)

        self.ui.tabWidget.setCurrentIndex(0)

        self._fill_versions()
        try:
            name = LEVEL_NAMES[settings.log_level()]
        except KeyError:
            name = 'INFO'
        self.ui.combo_log_level.setCurrentText(name)
        self.ui.combo_log_level.currentIndexChanged.connect(
            self._on_log_level_changed)
        self.adjustSize()
        self.ui.bt_clear_logs.clicked.connect(self._clear_logs)

    def _fill_versions(self):
        vdict = versions.get_versions()
        self.ui.table_versions.setRowCount(len(vdict.items()))
        for i, (k, v) in enumerate(sorted(vdict.items(), key=lambda x: x[0])):
            ver = QtWidgets.QTableWidgetItem()
            ver.setText(v)
            self.ui.table_versions.setItem(i, 0, ver)
        self.ui.table_versions.setVerticalHeaderLabels(
            sorted(vdict.keys()))

    def _on_log_level_changed(self, index):
        name = self.ui.combo_log_level.itemText(index)
        lvl = LEVELS_VALUES[name]
        settings.set_log_level(lvl)
        logging.getLogger().setLevel(lvl)

    def _clear_logs(self):
        logger.do_roll_over()
        for i in range(6):
            filename = 'hackedit.log%s' % ('' if not i else '.%d' % i)
            pth = os.path.join(os.path.dirname(logger.get_path()), filename)
            try:
                os.remove(pth)
            except OSError:
                if os.path.exists(pth):
                    _logger().exception('failed to remove log file %r', pth)
        QtWidgets.QMessageBox.information(self, 'Logs cleared',
                                          'Log files have been cleared.')
        self.ui.edit_log.clear()

    @staticmethod
    def show_about(parent):
        DlgAbout(parent).exec_()


def _logger():
    return logging.getLogger(__name__)
