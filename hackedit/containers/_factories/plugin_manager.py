

class PluginManagerFactory:
    def __call__(self, *args, **kwargs):
        from hackedit.application.services.plugin_manager import PluginManager
        return PluginManager()
