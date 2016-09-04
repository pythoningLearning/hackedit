from PyQt5 import QtWidgets

from PyQt5 import QtCore

from PyQt5 import QtGui

import pytest

from hackedit.application import plugins


def test_plugin_metadata():
    m = plugins.PluginMetadata('test')
    assert m.category == 'test'
    assert m.entry_point == 'hackedit.plugins.test'


class TestEditorPlugin:
    @classmethod
    def setup_class(cls):
        cls.plugin = plugins.EditorPlugin()

    def test_metadata(self):
        assert self.plugin.METADATA.category == 'editors'
        assert self.plugin.METADATA.entry_point == 'hackedit.plugins.editors'

    def test_editor_get_editor_class(self):
        with pytest.raises(NotImplementedError):
            assert self.plugin.get_editor_class()

    def test_get_specific_preferences_page(self):
        assert self.plugin.get_specific_preferences_page() is None

    def test_apply_specific_preferences(self):
        assert self.plugin.apply_specific_preferences(None) is None


class TestFileIconProviderPlugin:
    @classmethod
    def setup_class(cls):
        cls.plugin = plugins.FileIconProviderPlugin()

    def test_metadata(self):
        assert self.plugin.METADATA.category == 'file_icon_providers'
        assert self.plugin.METADATA.entry_point == 'hackedit.plugins.file_icon_providers'

    def test_icon(self):
        assert isinstance(self.plugin.icon(None), QtGui.QIcon)


class TestWorkspacePlugin():
    @classmethod
    def setup_class(cls):
        cls.plugin = plugins.WorkspacePlugin(None)

    def test_metadata(self):
        assert self.plugin.METADATA.category == 'workspace_plugins'
        assert self.plugin.METADATA.entry_point == 'hackedit.plugins.workspace_plugins'

    def test_has_main_window_attribute(self):
        assert hasattr(self.plugin, 'main_window')

    def test_activate(self):
        with pytest.raises(NotImplementedError):
            self.plugin.activate()

    def test_close(self):
        assert self.plugin.close() is None

    def test_get_preferences_page(self):
        assert self.plugin.get_preferences_page() is None

    def test_apply_preferences(self):
        assert self.plugin.apply_preferences() is None


class TestWorkspaceProviderPlugin:
        @classmethod
        def setup_class(cls):
            cls.plugin = plugins.WorkspaceProviderPlugin()

        def test_metadata(self):
            assert self.plugin.METADATA.category == 'workspace_providers'
            assert self.plugin.METADATA.entry_point == 'hackedit.plugins.workspace_providers'

        def test_get_data(self):
            assert isinstance(self.plugin.get_data(), dict)


class TestSymbolParserPlugin:
    @classmethod
    def setup_class(cls):
        cls.plugin = plugins.SymbolParserPlugin()

    def test_metadata(self):
        assert self.plugin.METADATA.category == 'symbol_parsers'
        assert self.plugin.METADATA.entry_point == 'hackedit.plugins.symbol_parsers'
        assert isinstance(self.plugin.mimetypes, list)

    def test_parse(self):
        assert isinstance(self.plugin.parse(''), list)


class TestPreferencePagePlugin:
    @classmethod
    def setup_class(cls):
        cls.plugin = plugins.PreferencePagePlugin()

    def test_metadata(self):
        assert self.plugin.METADATA.category == 'preference_pages'
        assert self.plugin.METADATA.entry_point == 'hackedit.plugins.preference_pages'

    def test_get_preferences_page(self):
        assert self.plugin.get_preferences_page() is None


class TestTemplateProviderPlugin:
    @classmethod
    def setup_class(cls):
        cls.plugin = plugins.TemplateProviderPlugin()

    def test_metadata(self):
        assert self.plugin.METADATA.category == 'template_providers'
        assert self.plugin.METADATA.entry_point == 'hackedit.plugins.template_providers'

    def test_get_label(self):
        assert self.plugin.get_label() == ''

    def test_get_url(self):
        assert self.plugin.get_url() == ''


class TestCompilerPlugin:
    @classmethod
    def setup_class(cls):
        cls.plugin = plugins.CompilerPlugin()

    def test_metadata(self):
        assert self.plugin.METADATA.category == 'compilers'
        assert self.plugin.METADATA.entry_point == 'hackedit.plugins.compilers'

    def test_get_compiler_icon(self):
        assert isinstance(self.plugin.get_compiler_icon(), QtGui.QIcon)

    def test_get_compiler(self):
        with pytest.raises(NotImplementedError):
            self.plugin.get_compiler()

    def test_get_compiler_config_widget(self):
        with pytest.raises(NotImplementedError):
            self.plugin.get_compiler_config_widget()

    def test_get_auto_detected_configs(self):
        with pytest.raises(NotImplementedError):
            self.plugin.get_auto_detected_configs()

    def test_create_new_configuration(self):
        with pytest.raises(NotImplementedError):
            self.plugin.create_new_configuration('config_name', '/usr/bin/cobc', extra_options={'test': '1'})

    def test_create_new_configuration_with_dialog_accepted(self, mock):
        mock.patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName', new=lambda x, y: ('path', None))
        with pytest.raises(NotImplementedError):
            self.plugin.create_new_configuration_with_dialog(None, 'config_name')

    def test_create_new_configuration_with_dialog_rejected(self, mock):
        mock.patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName', new=lambda x, y: ('', None))
        assert self.plugin.create_new_configuration_with_dialog(None, 'config_name') is None


class TestPreCompilerPlugin:
    @classmethod
    def setup_class(cls):
        cls.plugin = plugins.PreCompilerPlugin()

    def test_metadata(self):
        assert self.plugin.METADATA.category == 'pre_compilers'
        assert self.plugin.METADATA.entry_point == 'hackedit.plugins.pre_compilers'

    def test_get_pre_compiler_icon(self):
        assert isinstance(self.plugin.get_pre_compiler_icon(), QtGui.QIcon)

    def test_get_pre_compiler_type_name(self):
        with pytest.raises(NotImplementedError):
            self.plugin.get_pre_compiler_type_name()

    def test_get_pre_compiler_mimetypes(self):
        with pytest.raises(NotImplementedError):
            self.plugin.get_pre_compiler_mimetypes()

    def test_get_auto_detected_configs(self):
        with pytest.raises(NotImplementedError):
            self.plugin.get_auto_detected_configs()

    def test_create_new_configuration(self):
        with pytest.raises(NotImplementedError):
            self.plugin.create_new_configuration('config_name', '/usr/bin/cobc', extra_options={'test': '1'})

    def test_create_new_configuration_with_dialog_accepted(self, mock):
        mock.patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName', new=lambda x, y: ('path', None))
        with pytest.raises(NotImplementedError):
            self.plugin.create_new_configuration_with_dialog(None, 'config_name')

    def test_create_new_configuration_with_dialog_rejected(self, mock):
        mock.patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName', new=lambda x, y: ('', None))
        assert self.plugin.create_new_configuration_with_dialog(None, 'config_name') is None


class TestInterpreterPlugin:
    @classmethod
    def setup_class(cls):
        cls.plugin = plugins.InterpreterPlugin()

    def test_metadata(self):
        assert self.plugin.METADATA.category == 'interpreters'
        assert self.plugin.METADATA.entry_point == 'hackedit.plugins.interpreters'

    def test_get_interpreter_icon(self):
        with pytest.raises(NotImplementedError):
            self.plugin.get_interpreter_icon()

    def test_get_interpreter_type_name(self):
        with pytest.raises(NotImplementedError):
            self.plugin.get_interpreter_type_name()

    def test_get_interpreter_mimetypes(self):
        with pytest.raises(NotImplementedError):
            self.plugin.get_interpreter_mimetypes()

    def test_get_auto_detected_configs(self):
        with pytest.raises(NotImplementedError):
            self.plugin.get_auto_detected_configs()

    def test_create_new_configuration(self):
        with pytest.raises(NotImplementedError):
            self.plugin.create_new_configuration('config_name', '/usr/bin/cobc', extra_options={'test': '1'})

    def test_create_new_configuration_with_dialog_accepted(self, mock):
        mock.patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName', new=lambda x, y: ('path', None))
        with pytest.raises(NotImplementedError):
            self.plugin.create_new_configuration_with_dialog(None, 'config_name')

    def test_create_new_configuration_with_dialog_rejected(self, mock):
        mock.patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName', new=lambda x, y: ('', None))
        assert self.plugin.create_new_configuration_with_dialog(None, 'config_name') is None

    def test_get_package_manager(self):
        assert self.plugin.get_package_manager(None) is None