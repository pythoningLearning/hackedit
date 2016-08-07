from . import properties


class SettingsSection:
    def __init__(self, name, qsettings):
        """
        :param name: name of the settings section

        :param qsettings: qsettings instance
        :type qsettings: PyQt5.QtCore.QSettings
        """
        self._name = name
        self._qsettings = qsettings
        self._properties = {}
        self.add_properties(self.get_defaults())

    def get_defaults(self):
        raise NotImplementedError()

    def restore_defaults(self):
        for name, value in self.get_defaults().items():
            setattr(self, name, value)

    def get_value(self, key, default=''):
        return self._qsettings.value(self._get_section_key(key), default)

    def _get_section_key(self, key):
        return '%s/%s' % (self._name, key)

    def set_value(self, key, value):
        self._qsettings.setValue(self._get_section_key(key), value)

    def add_properties(self, properties_dic):
        for name, default in properties_dic.items():
            self.add_property(name, default)

    def add_property(self, name, default):
        if default is None:
            raise ValueError('default cannot be None')
        basic_properties = {
            bool: properties.BoolProperty,
            int: properties.IntProperty,
            str: properties.StringProperty,
        }
        try:
            property_class = basic_properties[type(default)]
        except KeyError as e:
            raise ValueError('property of type %r not supported (name=%r)' % (type(default), name))
        return self._add_property(property_class(name, default))

    def _add_property(self, prop):
        prop.section = self
        setattr(type(self), prop.name, property(fget=prop.get, fset=prop.set))
        self._properties[prop.name] = prop
        return getattr(self, prop.name)
