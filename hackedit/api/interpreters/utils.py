from hackedit.api.utils import memoize_args


def check_interpreter(interpreter):
    """
    Check if the interpreter instance works. The result is cached to prevent testing configurations that have already
    been tested.

    :raises: InterpreterCheckFailedError
    """
    classname = interpreter.__class__.__name__
    json_config = interpreter.config.to_json()
    _perform_check(classname, json_config, interpreter=interpreter)


def get_interpreter_version(interpreter, include_all=False):
    """
    Gets the version of the specified compiler and cache the results to prevent from running the compiler process
    uselessy.

    :returns: the compiler's version
    """
    path = interpreter.config.command
    return _get_version(path, include_all, interpreter=interpreter)


@memoize_args
def _perform_check(classname, json_config, interpreter=None):
    assert classname
    assert json_config
    interpreter.check()


@memoize_args
def _get_version(interpreter_path, include_all, interpreter=None):
    assert interpreter_path
    return interpreter.get_version(include_all=include_all)
