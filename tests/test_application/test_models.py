import json

from hackedit.application.models.file import FileModel, CompilableFileModel
from hackedit.application.models.project import InterpretedProjectModel, CompiledProjectModel
from hackedit.application.models.run_configs import ScriptRunConfigModel, RunConfigModel
from hackedit.application.models.solution import SolutionModel, ProjectPathModel

interpreted_project_content = '''{
    "build-commands": [
        "$interpreter setup.py build_ui"
    ],
    "build-system": "hebuild",
    "files": [
        {
            "path": "bootstrap.pyw",
            "type": "Script",
            "virtual-folder": "Sources"
        },
        {
            "path": "hackedit/__init__.py",
            "type": "Script",
            "virtual-folder": "Sources"
        },
        {
            "path": "README.rst",
            "type": "File",
            "virtual-folder": "Other"
        }
    ],
    "icon": "text/x-python",
    "interpreter": "Python3 (System)",
    "interpreter-typename": "Python",
    "name": "hackedit",
    "run-configurations": [
        {
            "environment-variables": {
                "TEST": "1"
            },
            "interpreter-arguments": [
                "--verbose"
            ],
            "name": "bootstrap",
            "script": "bootstrap.pyw",
            "script-arguments": [
                "--dev"
            ],
            "working-directory": "."
        }
    ],
    "type": "InterpretedProject",
    "virtual-folders": [
        "Sources"
    ]
}'''


class TestInterpretedProject():
    def test_deserialize(self):
        project = InterpretedProjectModel()
        project.deserialize(json.loads(interpreted_project_content))
        assert project.build_system == 'hebuild'
        assert project.name == 'hackedit'
        assert project.build_commands == ["$interpreter setup.py build_ui"]
        assert len(project.files) == 3
        assert isinstance(project.files[0], FileModel)
        assert project.files[0].path == 'bootstrap.pyw'
        assert project.files[0].virtual_folder == 'Sources'
        assert project.files[1].path == 'hackedit/__init__.py'
        assert project.files[1].virtual_folder == 'Sources'
        assert project.icon == 'text/x-python'
        assert project.interpreter == 'Python3 (System)'
        assert project.interpreter_type_name == 'Python'
        assert len(project.run_configs) == 1
        assert isinstance(project.run_configs[0], ScriptRunConfigModel)
        assert project.run_configs[0].name == 'bootstrap'
        assert project.run_configs[0].script == 'bootstrap.pyw'
        assert project.run_configs[0].script_arguments == ['--dev']
        assert project.run_configs[0].interpreter_arguments == ['--verbose']
        assert project.run_configs[0].environment_variables == {'TEST': '1'}
        assert project.run_configs[0].working_directory == '.'
        assert project.type == 'InterpretedProject'
        assert len(project.virtual_folders) == 1
        assert project.virtual_folders[0] == 'Sources'

    def test_serialize(self):
        project = InterpretedProjectModel()
        project.deserialize(json.loads(interpreted_project_content))
        result = json.dumps(project.serialize(), indent=4, sort_keys=True)
        assert result == interpreted_project_content


compiled_project_content = '''{
    "build-configurations": [
        {
            "build-steps": {
                "post": "",
                "pre": ""
            },
            "name": "Debug",
            "output-directory": "bin/Debug",
            "overrides": {
                "flags": "-debug"
            }
        },
        {
            "build-steps": {
                "post": "",
                "pre": ""
            },
            "name": "Release",
            "output-directory": "bin/Release",
            "overrides": {
                "flags": "-O2"
            }
        }
    ],
    "build-system": "hebuild",
    "compiler": "GnuCOBOL (System)",
    "compiler-typename": "GnuCOBOL",
    "files": [
        {
            "overrides": {
                "flags": "-Wall"
            },
            "path": "hello.cbl",
            "type": "Compilable",
            "virtual-folder": "Sources"
        },
        {
            "overrides": {},
            "path": "test/test.cbl",
            "type": "Compilable",
            "virtual-folder": "Sources"
        }
    ],
    "icon": "text/x-cobol",
    "multiple-executables": true,
    "name": "compiled cobol",
    "run-configurations": [
        {
            "environment-variables": {
                "TEST": "1"
            },
            "name": "hello",
            "program": "hello",
            "program-arguments": [
                "--verbose"
            ],
            "working-directory": ""
        },
        {
            "environment-variables": {},
            "name": "test",
            "program": "test",
            "program-arguments": [],
            "working-directory": ""
        }
    ],
    "type": "CompiledProject",
    "virtual-folders": [
        "Sources"
    ]
}'''


class TestCompiledProject():
    def test_deserialize(self):
        project = CompiledProjectModel()
        project.deserialize(json.loads(compiled_project_content))
        assert project.build_system == 'hebuild'
        assert project.name == 'compiled cobol'
        assert len(project.files) == 2
        assert isinstance(project.files[0], CompilableFileModel)
        assert project.files[0].path == 'hello.cbl'
        assert project.files[0].virtual_folder == 'Sources'
        assert project.files[0].overrides == {'flags': '-Wall'}
        assert project.files[1].path == 'test/test.cbl'
        assert project.files[1].virtual_folder == 'Sources'
        assert project.files[1].overrides == {}
        assert project.icon == 'text/x-cobol'
        assert project.compiler == 'GnuCOBOL (System)'
        assert project.compiler_type_name == 'GnuCOBOL'
        assert len(project.run_configs) == 2
        assert isinstance(project.run_configs[0], RunConfigModel)
        assert project.run_configs[0].name == 'hello'
        assert project.run_configs[0].program == 'hello'
        assert project.run_configs[0].program_arguments == ['--verbose']
        assert project.run_configs[0].environment_variables == {'TEST': '1'}
        assert project.run_configs[0].working_directory == ''
        assert project.run_configs[1].name == 'test'
        assert project.run_configs[1].program == 'test'
        assert project.run_configs[1].program_arguments == []
        assert project.run_configs[1].environment_variables == {}
        assert project.run_configs[1].working_directory == ''
        assert project.type == 'CompiledProject'
        assert len(project.virtual_folders) == 1
        assert project.virtual_folders[0] == 'Sources'

    def test_serialize(self):
        project = CompiledProjectModel()
        project.deserialize(json.loads(compiled_project_content))
        result = json.dumps(project.serialize(), indent=4, sort_keys=True)
        assert result == compiled_project_content


solution_content = '''{
    "name": "Test",
    "projects": [
        {
            "path": "TestProj1/testproj1.heproj",
            "virtual-folder": "Presentation"
        },
        {
            "path": "TestProj2/testproj2.heproj",
            "virtual-folder": "Application"
        },
        {
            "path": "TestProj3/testproj3.heproj",
            "virtual-folder": "Infrastructure"
        }
    ],
    "virtual-folders": [
        "Presentation",
        "Application",
        "Infrastructure"
    ]
}'''


class TestSolutionMOdel:
    def test_deserialize(self):
        solution = SolutionModel()
        solution.deserialize(json.loads(solution_content))
        assert solution.name == 'Test'
        assert len(solution.projects) == 3
        assert isinstance(solution.projects[0], ProjectPathModel)
        assert solution.projects[0].path == "TestProj1/testproj1.heproj"
        assert solution.projects[0].virtual_folder == "Presentation"
        assert solution.projects[1].path == "TestProj2/testproj2.heproj"
        assert solution.projects[1].virtual_folder == "Application"
        assert solution.projects[2].path == "TestProj3/testproj3.heproj"
        assert solution.projects[2].virtual_folder == "Infrastructure"

    def test_serialize(self):
        solution = SolutionModel()
        solution.deserialize(json.loads(solution_content))
        result = json.dumps(solution.serialize(), indent=4, sort_keys=True)
        assert result == solution_content
