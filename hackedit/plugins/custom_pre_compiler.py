from hackedit.api.plugins import PreCompilerPlugin
from hackedit.api.pre_compiler import CustomPreCompilerConfig


class CustomPreCompilerPlugin(PreCompilerPlugin):
    def get_pre_compiler_type_name(self):
        return CustomPreCompilerConfig().type_name

    def get_auto_detected_configs(self):
        return []

    def create_new_configuration(self, name, path):
        cfg = CustomPreCompilerConfig()
        cfg.path = path
        cfg.name = name
        return cfg
