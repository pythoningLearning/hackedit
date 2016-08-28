from hackedit.api import mixins


class PreCompilerConfig(mixins.JSonisable, mixins.Copyable):
    def __init__(self):
        #: name of the configuration
        self.name = ''

        #: path of the pre-compiler
        self.path = ''

        #: the associated mimetypes, specify the file extensions supported by the pre-compiler
        self.mimetypes = []

        #: the list of pre-compiler flags
        self.flags = []

        #: the pre-compiler output pattern, used to deduce the pre-compiler output file path
        #:
        #: E.g.::
        #:
        #:    $input_file_name.abc (file.xyz -> file.abc)
        #:
        self.output_pattern = ''

        #: describes how to build the pre compiler command
        #: the following macros can be used:
        #:    - $input_file
        #:    - $input_file_name
        #:    - $output_file
        #:    - $output_file_name
        #:    - $flags
        #:
        self.command_pattern = ''

        #: the content of the test file used to test the pre-compiler automatically
        self.test_file_content = ''

        #: the arguments needed to check the version:
        self.version_command_args = []

        #: the regex used to extract the version info from the version_command output
        self.version_regex = r'(?P<version>\d\.\d\.\d)'

        #: PreCompiler type name
        self.type_name = ''
