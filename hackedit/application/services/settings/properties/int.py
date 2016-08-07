from .base import SettingsProperty


class IntProperty(SettingsProperty):
    def _get(self):
        return int(self.section.get_value(self.name, default=self.default_value))

    def _set(self, value):
        self.section.set_value(self.name, int(value))
