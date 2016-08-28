from hackedit.application.utilities.decorators import memoize_args


def check_pre_compiler(pre_compiler):
    """
    Check if the compiler instance works. The result is cached to prevent testing configurations that have already
    been tested.

    :raises: CompilerCheckFailedError in case of failure
    """
    classname = pre_compiler.__class__.__name__
    json_config = pre_compiler.config.to_json()
    _perform_check(classname, json_config, pre_compiler=pre_compiler)


def get_pre_compiler_version(pre_compiler, include_all=False):
    """
    Gets the version of the specified compiler and cache the results to prevent from running the compiler process
    uselessy.

    :returns: the compiler's version
    """
    path = pre_compiler.config.path
    return _get_version(path, include_all, pre_compiler=pre_compiler)


@memoize_args
def _perform_check(classname, json_config, pre_compiler=None):
    if pre_compiler:
        pre_compiler.check_pre_compiler()


@memoize_args
def _get_version(compiler_path, include_all, pre_compiler=None):
    if pre_compiler:
        return pre_compiler.get_version(include_all=include_all)
    return ''
