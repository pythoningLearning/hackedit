from hackedit.containers import Services


class TestPluginManager:
    @classmethod
    def setup_class(cls):
        cls.plugin_manager = Services.plugin_manager()

    def test_get_plugins(self):
        assert isinstance(self.plugin_manager.get_plugins('editors'), dict)

    def test_get_plugin(self):
        assert self.plugin_manager.get_plugin('editors', 'CobolCodeEditPlugin') is not None
