import pkg_resources
from hackedit.containers import Services
from hackedit.api.plugins import PluginMetadata


class TestPluginLoader:
    @classmethod
    def setup_class(cls):
        cls.loader = Services.plugin_loader()

    def test_load_plugins_valid_meta(self):
        meta = PluginMetadata('editors')
        plugins, failures = self.loader.load_plugins(meta)
        assert plugins
        assert not failures

    def test_load_plugins_invalid_meta(self):
        meta = PluginMetadata('test')
        plugins, failures = self.loader.load_plugins(meta)
        assert not plugins
        assert not failures

    def test_load_valid_entrypoint(self):
        failures = {}
        plugins = {}
        entry_point = list(pkg_resources.iter_entry_points('hackedit.plugins.editors'))[0]
        self.loader._load_entrypoint(entry_point, failures, plugins)
        assert plugins
        assert not failures

    def test_load_invalid_entrypoint(self):
        failures = {}
        plugins = {}
        self.loader._load_entrypoint('test', failures, plugins)
        assert not plugins
        assert failures
