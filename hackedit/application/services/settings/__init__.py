from PyQt5 import QtCore

from .environment import EnvironmentSettingsSection
from .editor import EditorSettingsSection


class Settings:
    def __init__(self):
        self._qsettings = QtCore.QSettings()
        self.sections = {}
        self.add_section('environment', EnvironmentSettingsSection(self._qsettings))
        self.add_section('editor', EditorSettingsSection(self._qsettings))

    def add_section(self, name, section):
        self.sections[name] = section
        setattr(self, name, section)

    def clear(self):
        self._qsettings.clear()
