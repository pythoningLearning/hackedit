"""
This module contains functions for easily setup the application logger
"""
import glob
import logging
import os

from hackedit.api import system

#: reference to the file handler
file_handler = None


def get_path():
    """
    Returns the log file path.

    - GNU/Linux: ``~/.hackedit/hackedit.log``
    - OSX: ``~/Library/Application Support/HackEdit/hackedit.log``
    - WINDOWS: ``%APPDATA%\HackEdit\hackedit.log``

    :return: str
    """
    from hackedit.api import system
    return os.path.join(system.get_app_data_directory(), 'hackedit-%d.log' % os.getpid())


def setup(level=logging.INFO):
    """
    Configures the logger, adds a stream handler and a file handler.

    :param level: log level, default is logging.INFO
    """
    global file_handler
    if len(get_log_files()) > 5:
        clear_logs()
    file_handler = logging.FileHandler(get_path())
    handlers = [
        # a new log will be created on each new day with 5 days backup
        file_handler,
        logging.StreamHandler()
    ]
    logging.basicConfig(
        level=logging.WARNING, handlers=handlers,
        format='%(asctime)s:%(msecs)03d::%(levelname)s::%(process)d::%(name)s'
        '::%(message)s', datefmt='%H:%M:%S')
    logging.getLogger().setLevel(level)
    logging.getLogger('hackedit').info('-' * 80)


def clear_logs():
    if file_handler:
        file_handler.close()
    failures = []
    for filename in get_log_files():
        pth = os.path.join(system.get_app_data_directory(), filename)
        try:
            os.remove(pth)
        except OSError:
            if os.path.exists(pth):
                logging.getLogger('open_cobol_ide').exception(
                    'failed to remove log file %r', pth)
                failures.append(pth)
    return failures


def get_log_files():
    return glob.glob(os.path.join(system.get_app_data_directory(), '*.log'))


def get_application_log():
    try:
        with open(get_path(), 'r') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return ''
