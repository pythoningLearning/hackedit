from dependency_injector.injections import inject

from hackedit.containers import Factories
from hackedit.application.factories.file import FileModelFactory

from .build_configs import BuildConfigModel
from .run_configs import RunConfigModel, ScriptRunConfigModel


class ProjectModel:
    """
    Model that stores the project properties (list of files, build configs,...).

    The model can be serialized/deserialized to/from a dict.

    Concrete projects can extend this class to add project specific properties.
    """
    def __init__(self):
        self.build_system = ''
        self.files = []
        self.icon = ''
        self.name = ''
        self.run_configs = []
        self.type = ''
        self.virtual_folders = []

    def serialize(self):
        return {
            'files': [file.serialize() for file in self.files],
            'icon': self.icon,
            'name': self.name,
            'type': self.type,
            'virtual-folders': self.virtual_folders,
            'run-configurations': [run_cfg.serialize() for run_cfg in self.run_configs],
            'build-system': self.build_system
        }

    def deserialize(self, data):
        self.build_system = data['build-system']
        self.files[:] = []
        for file in data['files']:
            self.files.append(self._deserialize_file(file))
        self.icon = data['icon']
        self.name = data['name']
        self.run_configs[:] = []
        for run_cfg in data['run-configurations']:
            self.run_configs.append(self._deserialize_run_config(run_cfg))
        self.type = data['type']
        self.virtual_folders = data['virtual-folders']
        return self

    def _deserialize_run_config(self, data):
        run_cfg = RunConfigModel()
        run_cfg.deserialize(data)
        return run_cfg

    @inject(file_model_factory=Factories.file_model_factory)
    def _deserialize_file(self, data, file_model_factory):
        return file_model_factory.deserialize(data)


class InterpretedProjectModel(ProjectModel):
    """
    Extends ProjectModel for interpreted projects (python, ruby,...) using our own build system (hebuild).
    """
    def __init__(self):
        super().__init__()
        self.build_system = 'hebuild'
        self.type = 'InterpretedProject'
        self.interpreter = ''
        self.interpreter_type_name = ''
        self.build_commands = []

    def serialize(self):
        data = super().serialize()
        data['interpreter'] = self.interpreter
        data['interpreter-typename'] = self.interpreter_type_name
        data['build-commands'] = self.build_commands
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.interpreter = data['interpreter']
        self.interpreter_type_name = data['interpreter-typename']
        self.build_commands = data['build-commands']
        return self

    def _deserialize_run_config(self, data):
        run_cfg = ScriptRunConfigModel()
        run_cfg.deserialize(data)
        return run_cfg


class CompiledProjectModel(ProjectModel):
    """
    Extends ProjectModel for compiled projects (python, C/C++,...) using our own build system (hebuild).
    """
    def __init__(self):
        super().__init__()
        self.build_system = 'hebuild'
        self.type = 'CompiledProject'
        self.multiple_executables = False
        self.compiler = ''
        self.compiler_type_name = ''
        self.build_configurations = []

    def serialize(self):
        data = super().serialize()
        data['compiler'] = self.compiler
        data['compiler-typename'] = self.compiler_type_name
        data['multiple-executables'] = self.multiple_executables
        data['build-configurations'] = [build_cfg.serialize() for build_cfg in self.build_configurations]
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.compiler = data['compiler']
        self.compiler_type_name = data['compiler-typename']
        self.multiple_executables = data['multiple-executables']
        self.build_configurations[:] = []
        for build_cfg in data['build-configurations']:
            self.build_configurations.append(self._deserialize_build_config(build_cfg))
        return self

    def _deserialize_build_config(self, data):
        return BuildConfigModel().deserialize(data)
