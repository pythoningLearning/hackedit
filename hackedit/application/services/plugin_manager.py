import logging

from dependency_injector.injections import inject
from hackedit.application.plugins import plugin_types
from hackedit.containers import Services


class PluginManager:
    @inject(plugin_loader=Services.plugin_loader)
    def __init__(self, plugin_loader=None):
        self._plugins = {}
        self._failed_to_load = {}
        self._load_plugins(plugin_loader)

    def get_plugins(self, category):
        return self._plugins[category]

    def get_plugin(self, category, plugin_name):
        return self.get_plugins(category)[plugin_name]

    def _load_plugins(self, plugin_loader):
        for plugin in sorted(plugin_types(), key=lambda x: x.METADATA.category):
            plugins, failed_to_load = plugin_loader.load_plugins(plugin.METADATA)
            self._plugins[plugin.METADATA.category] = plugins
            self._failed_to_load.update(failed_to_load)


def _logger():
    return logging.getLogger(__name__)
