

class IPluginLoader:
    def load_plugins(self, plugin_metadata):
        """
        Loads all the plugins that match the specified plugin metadata.

        :type plugin_metadata: hackedot.application.plugins.PluginMetadata

        :return: a tuple of dict. The first dict contains the loaded plugins,
            the second dict contains the name of the plugins that failed to load with the exception that was raised.
        """
        raise NotImplementedError()
