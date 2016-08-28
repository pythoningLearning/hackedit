from hackedit.api import mixins


class CompilerConfig(mixins.JSonisable, mixins.Copyable):
    """
    Stores a compiler configuration.
    """
    def __init__(self):
        #: Name of the configuration
        self.name = ''
        #: Directory where the compiler can be found, use an emtpy path to use the system configuration.
        self.compiler = ''
        #: The associated mimetypes, use to find a valid file compiler.
        self.mimetypes = []
        #: Compiler flags that will be appended to every compiler command.
        self.flags = []
        #: List of include paths (used for copybooks in COBOL).
        self.include_paths = []
        #: List of libraries to include
        self.library_paths = []
        #: List of libraries to link with
        self.libraries = []
        #: Custom environment variables
        self.environment_variables = {}
        self.vcvarsall = ''
        self.vcvarsall_arch = 'x86'
        #: type_name of the associated compiler
        self.type_name = ''

    def __repr__(self):
        return 'CompilerConfig(' + self.to_json() + ')\n'
