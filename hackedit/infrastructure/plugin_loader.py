import logging
import traceback

import pkg_resources
from hackedit.application.interfaces.plugin_loader import IPluginLoader


def _logger():
    return logging.getLogger(__name__)


class SetuptoolsPluginLoader(IPluginLoader):
    """
    Loads plugins using their setuptools entry-points.
    """
    def load_plugins(self, metadata):
        plugins = {}
        failed_to_load = {}

        _logger().info('loading plugin entrypoint: %s' % metadata.entry_point)
        for entry_point in pkg_resources.iter_entry_points(metadata.entry_point):
            self._load_entrypoint(entry_point, failed_to_load, plugins)

        return plugins, failed_to_load

    def _load_entrypoint(self, entry_point, failed_to_load, plugins):
        plugin_name = self._get_plugin_name(entry_point)
        _logger().info('  - loading plugin: %s', plugin_name)
        try:
            plugin_class = entry_point.load()
            plugin_instance = plugin_class()
        except Exception as e:
            _logger().exception('Failed to load plugin')
            failed_to_load[plugin_name] = traceback.format_exc(), e
        else:
            plugins[plugin_name] = plugin_instance

    @staticmethod
    def _get_plugin_name(entry_point):
        return str(entry_point).split('=')[0].strip()
