from .base import SettingsProperty


class StringProperty(SettingsProperty):
    def _get(self):
        return str(self.section.get_value(self.name, default=self.default_value))

    def _set(self, value):
        self.section.set_value(self.name, str(value))
