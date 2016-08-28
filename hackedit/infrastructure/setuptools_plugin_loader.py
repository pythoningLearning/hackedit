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
        _logger().info('loading plugins category: %s' % metadata.category)
        plugins = {}
        failed_to_load = {}
        entry_points = list(pkg_resources.iter_entry_points(metadata.entry_point))
        for entry_point in entry_points:
            name = str(entry_point).split('=')[0].strip()
            _logger().info('  - loading plugin: %s', name)
            try:
                plugin_class = entry_point.load()
                plugin_instance = plugin_class()
            except Exception as e:
                _logger().exception('Failed to load plugin')
                failed_to_load[name] = traceback.format_exc(), e
            else:
                plugins[name] = plugin_instance
        return plugins, failed_to_load
