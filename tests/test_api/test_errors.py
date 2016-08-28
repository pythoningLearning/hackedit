import logging

from hackedit.api import errors


def test_command_builder_failed_error():
    exc = errors.CommandBuildFailedError('my message')
    assert exc.message == 'my message'


def test_program_check_failed_error_with_error_level(mocker):
    mocker.spy(_logger(), 'error')
    exc = errors.ProgramCheckFailedError('test', _logger, 'an error message', -1)
    assert exc.error_level == errors.ProgramCheckFailedError.ERROR
    assert exc.message == 'an error message'
    assert exc.return_code == -1
    _logger().error.assert_called_once_with("test check failed: 'an error message'")


def test_program_check_failed_error_with_warning_level(mocker):
    mocker.spy(_logger(), 'warn')
    exc = errors.ProgramCheckFailedError('test', _logger, 'a warning message', -2,
                                         errors.ProgramCheckFailedError.WARNING)
    assert exc.error_level == errors.ProgramCheckFailedError.WARNING
    assert exc.message == 'a warning message'
    assert exc.return_code == -2
    _logger().warn.assert_called_once_with("test check failed: 'a warning message'")


def _logger():
    return logging.getLogger(__name__)

