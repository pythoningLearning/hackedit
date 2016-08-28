

class PluginLoaderFactory:
    def __call__(self, *args, **kwargs):
        from hackedit.infrastructure.plugin_loader import SetuptoolsPluginLoader
        return SetuptoolsPluginLoader()
