class SettingsProperty:
    def __init__(self, name, default_value):
        self.name = name
        self.default_value = default_value
        self.section = None

    def get(self, obj_type):
        return self._get()

    def set(self, obj_type, value):
        self._set(value)

    def _get(self):
        raise NotImplementedError()

    def _set(self, value):
        raise NotImplementedError()
