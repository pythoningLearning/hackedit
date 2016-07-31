"""
This module contains the plugin interface that you need to implement
for writing new plugins.

Plugins are regular python packages that contains a set of setuptools
entrypoints that expose the available plugins.

Basically you need to define a dictionary where the keys are the possible
entrypoints (one per plugin type) and the values the list of python classes
that implement the entrypoint interface.

This module describes the entrypoints interface, each "interface" has a
``ENTRYPOINT`` attribute, that is the string you need to use in the entrypoints
dict in your setup.py.

"""
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QObject

from . import _shared
from ._shared import _window


class EditorPlugin:
    """
    An editor plugin returns the CodeEdit class that needs to be registerd
    inside the application.
    """
    #: setuptools entry point to use for adding new editor plugins.
    ENTRYPOINT = 'hackedit.plugins.editors'

    @staticmethod
    def get_editor_class():
        """
        Returns the editor **class** to register.
        :return: a subclass of :class:`pyqode.core.api.CodeEdit`
        """
        pass

    @classmethod
    def get_specific_preferences_page(cls):
        """
        Returns a preferences page to edit the settings specific to your
        editor.
        """
        pass

    @classmethod
    def apply_specific_preferences(cls, editor):
        """
        Apply the specific preferences to an editor instance
        """
        pass


class FileIconProviderPlugin:
    """
    The file icon provider plugin provide a custom icon for a specific file
    extension. Implement this only if the mimetype for your file is not widely
    available in the icon themes.

    To define such a plugin, you need to define a list of supported
    extensions: :attr:SUPPORTED_EXTENSIONS and a function that will return the
    actual QIcon instance: :func:`icon`.
    """
    ENTRYPOINT = 'hackedit.plugins.file_icon_providers'

    #: the list of supported file extensions. Use the '.' extension for
    #: folders (e.g. if you need to display a custom icon for special folders
    #: such as python packages).
    SUPPORTED_EXTENSIONS = []

    def icon(self, file_info):
        """
        Returns the corresponding file icon

        :param file_info: QFileInfo
        :retype: PyQt5.QtGui.QIcon
        """
        pass


class WorkspacePlugin(QObject):
    """
    A workspace plugin is a generic window plugin but tied to a workspace.

    To create a workspace plugin: create a subclass and implement the following
    methods:

        - activate: setup your plugin
        - close: to stop any background task or close any resource that your
          plugin might use.
        - get_preferences_page (classmethod): returns a custom
          :class:`hackedit.widgets.PreferencePage` instance that will show up
          in the app's preferences dialog.
        - apply_preferences: to apply any custom preferences exposed by
          :func:`get_preferences_page` on the plugin instance.

    """

    #: setuptools entry point to use for adding new editor plugins.
    ENTRYPOINT = 'hackedit.plugins.workspace_plugins'

    def __init__(self, window):
        """
        :param window: Reference to the main window where the plugin has been
                       attached to.
        :type window: hackedit.app.gui.main_window.MainWindow
        """
        self.main_window = window
        super().__init__()

    def activate(self):
        """
        Activates the plugin.

        You should implement this method to setup your plugin (create widgets,
        connect signals/slots,...)
        """
        pass

    def close(self):
        """
        This method is called when the parent window has been closed.

        Implemented this method if you need to cleanup some resources or stop
        somes services,...
        """
        pass

    @classmethod
    def get_preferences_page(cls):
        """
        Returns the plugin config page. A page is a simple widget where you
        expose your plugin's preferences. That page will be automatically shown
        under the plugin node in the application's preferences dialog.

        .. warning: This is a classmethod!

        :rtype: hackedit.api.widgets.PreferencePage
        """
        pass

    def apply_preferences(self):
        """
        Apply user preferences to your plugin (the one exposed in your config
        page).
        """
        pass


class WorkspaceProviderPlugin:
    """
    A workspace provider plugin let you add some builtin workspaces to
    HackEdit.

    Just implement `get_data` to return a dictionary with the following
    structure::

        workspace = {
            name: 'Your workspace name',
            description: 'Your workspace description, can be multiline',
            plugins: ['PluginA', 'PluginB', ...]
        }

    """

    #: setuptools entry point to use for adding new editor plugins.
    ENTRYPOINT = 'hackedit.plugins.workspace_providers'

    def get_data(self):
        """
        Gets the workspace data dictionnary.
        """
        pass


class SymbolParserPlugin:
    """
    Plugin used to parse the symbols of a file.

    The plugin must declare the mimetypes it can handle and implement
    the ``parse`` method.

    The parse method will parse the content of a file and return a list
    of :class:`pyqode.core.share.Definition` that will be written to the
    project's index database by the indexing backend.
    """
    ENTRYPOINT = 'hackedit.plugins.symbol_parsers'

    #: Specify the mimetypes that can be handled by a particular indexor
    #: plugin
    mimetypes = []

    def parse(self, path):
        """
        Parses a file and returns a list of
        :class:`pyqode.core.share.Definition`.

        This method will be called automatically when indexing files for any
        file that match one of the supported mimetype.
        """
        pass


class PreferencePagePlugin:
    """
    A preference page plugin provides a :class:`PreferencePage` widget that
    will get automatically shown in the application preferences dialog.

    This preference page won't be tied to the plugins category (you're free to
    define a category or not in your preferences page).
    """

    #: setuptools entry point to use for adding new editor plugins.
    ENTRYPOINT = 'hackedit.plugins.preference_pages'

    @classmethod
    def get_preferences_page(cls):
        """
        Returns the preference page widget.
        """
        pass


class TemplateProviderPlugin:
    """
    A template provider plugin provides an additional source of templates
    to the application.
    """
    ENTRYPOINT = 'hackedit.plugins.template_providers'

    def get_label(self):
        """
        Gets the label of the provider. The label will appear in the list
        of template sources. It must be carefully chosen.
        """
        pass

    def get_url(cls):
        """
        Gets the template url. This can be a remote url (pointing to a git
        repository) or a local url (pointing to the directory that contains the
        templates)
        """
        pass


class CompilerPlugin:
    """
    Adds support for a new compiler in HackEdit.
    """
    ENTRYPOINT = 'hackedit.plugins.compilers'

    def get_compiler_icon(self):
        from hackedit.api import special_icons
        return special_icons.run_build()

    def get_compiler(self):
        """
        Gets the associated compiler instance that inherit from :class:`hackedit.api.compilers.Compiler`.
        """
        raise NotImplementedError()

    def get_compiler_config_widget(self):
        """
        Gets the associated compiler configuration widget that inherit from
        :class:`hackedit.api.compilers.CompilerConfigurationWidget`.
        """
        raise NotImplementedError()

    def get_auto_detected_configs(self):
        """
        Get the list of autodetected compiler configurations.
        """
        raise NotImplementedError()

    def _select_compiler_path(self, parent):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(parent, 'Select compiler')
        if path:
            return True, path
        return False, ''

    def create_new_configuration_with_dialog(self, parent, name):
        """
        Creates a new compiler configuration with the ability to show a wizard/dialog to ask more inputs from the user.

        The default implementation just asks for the compiler path but you can overwrite it to show your own dialog

        This method should rely on `create_new_configuration` to create the final configuration.
        """
        status, path = self._select_compiler_path(parent)
        if not status:
            return None
        return self.create_new_configuration(name, path)

    def create_new_configuration(self, name, compiler_path, extra_options=None):
        """
        Creates a new configuration.

        :param name: unique name of the configuration.
        :param compiler_path: compiler path or command
        :param extra_options: optional extra options
        """
        raise NotImplementedError()


class PreCompilerPlugin:
    """
    Adds support for a new pre-compiler in HackEdit.
    """

    ENTRYPOINT = 'hackedit.plugins.pre_compilers'

    def get_pre_compiler_icon(self):
        return QtGui.QIcon.fromTheme('database-index')

    def get_pre_compiler_type_name(self):
        raise NotImplementedError()

    def get_pre_compiler_mimetypes(self):
        raise NotImplementedError()

    def get_auto_detected_configs(self):
        """
        Get the list of autodetected compiler configurations.
        """
        raise NotImplementedError()

    def create_new_configuration_with_dialog(self, parent, name):
        """
        Creates a new configuration with the ability to show a wizard/dialog to ask more inputs from the user.

        The default implementation just asks for the compiler path but you can overwrite it to show your own dialog.

        This method should rely on `create_new_configuration` to create the final configuration.
        """
        status, path = self._select_pre_compiler_path(parent)
        if not status:
            return None
        return self.create_new_configuration(name, path)

    def create_new_configuration(self, name, path, extra_options):
        """
        Creates a new configuration.

        :param name: unique name of the configuration.
        """
        raise NotImplementedError()

    def _select_pre_compiler_path(self, parent):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(parent, 'Select pre-compiler')
        if path:
            return True, path
        return False, ''


def get_plugin_instance(plugin_class):
    """
    Returns the plugin instance that match a given plugin **class**.

    :param plugin_class: Plugin class
    """
    return _window().get_plugin_instance(plugin_class)


def get_compiler_plugins():
    """
    Returns a list of all known compiler plugins.

    :rtype: [CompilerPlugin]
    """
    ret_val = []
    for plugin in _shared.APP.plugin_manager.compiler_plugins.values():
        ret_val.append(plugin)
    return ret_val


def get_compiler_plugin_by_typename(compiler_type_name):
    """
    Gets the compiler plugin that match the specified compiler_type_name.

    :rtype: CompilerPlugin
    """
    try:
        return _shared.APP.plugin_manager.compiler_plugins[compiler_type_name]
    except KeyError:
        return None


def get_compiler_plugin_by_mimetype(mimetype):
    """
    Gets the compiler plugin that match the specified mimetype

    :rtype: CompilerPlugin
    """
    for plugin in get_compiler_plugins():
        if mimetype in plugin.get_compiler().mimetypes:
            return plugin
    return None


def get_pre_compiler_plugins():
    """
    Returns a list of all known pre-compiler plugins

    :rtype: [PreCompilerPlugin]
    """
    ret_val = []
    for plugin in _shared.APP.plugin_manager.pre_compiler_plugins.values():
        ret_val.append(plugin)
    return ret_val


def get_pre_compiler_plugin_by_typename(pre_compiler_type_name):
    """
    Gets the pre-compiler plugin that match the specified pre_compiler_type_name.

    :rtype: PreCompilerPlugin
    """
    try:
        return _shared.APP.plugin_manager.pre_compiler_plugins[pre_compiler_type_name]
    except TypeError:
        return None


def get_pre_compiler_plugin_by_mimetype(mimetype):
    """
    Gets the pre-compiler plugin that matches the specified mimetype

    :rtype: PreCompilerPlugin
    """
    for plugin in get_pre_compiler_plugins():
        if mimetype in plugin.get_pre_compiler_mimetypes():
            return plugin
    return None


def get_script_runner():
    """
    Gets the script runner plugin instance if any otherwise returns None.

    :rtype: hackedit.api.interpreters.ScriptRunnerPlugin
    """
    from .interpreters import ScriptRunnerPlugin

    return _window().get_plugin_instance(ScriptRunnerPlugin)
