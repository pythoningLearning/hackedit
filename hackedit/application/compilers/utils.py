from hackedit.application.utilities.decorators import memoize_args


def check_compiler(compiler):
    """
    Check if the compiler instance works. The result is cached to prevent testing configurations that have already
    been tested.

    :raises: CompilerCheckFailedError in case of failure
    """
    classname = compiler.__class__.__name__
    json_config = compiler.config.to_json()
    _perform_check(classname, json_config, compiler=compiler)


def get_compiler_version(compiler, include_all=False):
    """
    Gets the version of the specified compiler and cache the results to prevent from running the compiler process
    uselessy.

    :returns: the compiler's version
    """
    path = compiler.get_full_compiler_path()
    return _get_version(path, include_all, compiler=compiler)


@memoize_args
def _perform_check(classname, json_config, compiler=None):
    compiler.check_compiler()


@memoize_args
def _get_version(compiler_path, include_all, compiler=None):
    return compiler.get_version(include_all=include_all)

