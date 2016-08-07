import os
from fnmatch import fnmatch

from dependency_injector.injections import inject
from hackedit.containers import Services


def is_outdated(source, destination, working_dir=''):
    """
    Checks if the destination is outdated (i.e. the source is newer than the destination).
    """
    try:
        if not os.path.isabs(source):
            source = os.path.join(working_dir, source)
        if not os.path.isabs(destination):
            destination = os.path.join(working_dir, destination)
        try:
            return os.path.getmtime(source) > os.path.getmtime(destination)
        except OSError:
            return True
    except (TypeError, AttributeError):
        raise ValueError('Invalid source and destinations')


@inject(settings=Services.settings)
def is_ignored_path(path, ignore_patterns=None, settings=None):
    """
    Utility function that checks if a given path should be ignored.

    A path is ignored if it matches one of the ignored_patterns.

    :param path: The path to check.
    :param ignore_patterns: The ignore patters to respect. If None, the ignore patterns of the application
        settings will be used.
    :returns: True if the path is in a directory that must be ignored or if the file name matches an ignore pattern,
        otherwise returns False.
    """
    if ignore_patterns is None:
        ignore_patterns = settings.environment.ignored_patterns.split(';')

    def ignore(name):
        for ptrn in ignore_patterns:
            if fnmatch(name, ptrn):
                return True

    for part in os.path.normpath(path).split(os.path.sep):
        if part and ignore(part):
            return True
    return False
