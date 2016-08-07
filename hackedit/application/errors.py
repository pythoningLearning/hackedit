import logging


class CommandBuildFailedError(Exception):
    def __init__(self, message):
        self.message = message


class ProgramCheckFailedError(Exception):
    WARNING = 0
    ERROR = 1

    def __init__(self, program, logger, message, return_code=None, error_level=None):
        if error_level is None:
            error_level = self.ERROR
        self.error_level = error_level
        self.message = message
        self.return_code = return_code
        if self.error_level == self.WARNING:
            log_fct = logger().warn
        else:
            log_fct = logger().error
        log_fct('%s check failed: %r' % (program, self.message))


class CompilerCheckFailedError(ProgramCheckFailedError):
    def __init__(self, *args, **kwargs):
        def _logger():
            return logging.getLogger('compiler')

        super().__init__('Compiler', _logger, *args, **kwargs)


class InterpreterCheckFailed(ProgramCheckFailedError):
    def __init__(self, type_name, *args, **kwargs):
        def _logger():
            return logging.getLogger('interpreters')

        super().__init__(type_name, _logger, *args, **kwargs)
