"""
This module contains the backend function that perform the actual indexation.

Those functions are run in a background task.
"""
import functools
import logging
import mimetypes
import os
import time
from fnmatch import fnmatch

from pyqode.core.share import Definition

from hackedit.api import utils
from hackedit.app import mime_types
from hackedit.app.index import db


try:
    # new scandir function in python 3.5
    from os import scandir as listdir
except ImportError:
    try:
        # new scandir function from _scandir package on pypi
        from scandir import scandir as listdir
    except ImportError:
        # scandir function not found, use the slow listdir function
        from os import listdir


def index_project_files(task_handle, project_directories, ignore_patterns,
                        parser_plugins):
    """
    Perform project files indexation.

    :param task_handle: TaskHandle to report task progress.
    :param project_directory: Project directory to indexate.
    :param ignore_patterns: The ignore patterns to respect.
    """
    mime_types.load()
    # adjust ignore patterns to always exclude binary files from indexation
    ignore_patterns += ['*.exe', '*.dll', '*.usr', '*.so', '*.dylib', '*.psd',
                        '*.db', '.hackedit', '.eggs', '.cache', '.git', '.svn',
                        '.hackedit', 'build', 'dist', '_build']

    symbol_ignored_patterns = ['*.png', '*.jpg', '*.tga', '*.svg', '*.ui']
    parser_plugins = tuple(parser_plugins)
    # create projects
    proj_ids = []

    task_handle.report_progress(_('Creating projects'), -1)
    with db.DbHelper() as dbh:
        for project_directory in project_directories:
            proj_ids.append((dbh.create_project(project_directory),
                             project_directory))

    # create file index
    for proj_id, project_directory in proj_ids:
        # scan project dir recursively
        task_handle.report_progress(_('Indexing project directories: %r') %
                                    project_directory, -1)
        files = []
        paths = scandir(task_handle, project_directory, ignore_patterns,
                        os.path.dirname(project_directory))
        with db.DbHelper() as dbh:
            for path in paths:
                fid = dbh.create_file(path, proj_id, commit=False)
                files.append((path, fid, project_directory))
            dbh.conn.commit()

        # parse each document
        task_handle.report_progress(_('Indexing project files: %r') %
                                    project_directory, -1)
        for file_path, file_id, root_directory in files:
            ext = os.path.splitext(file_path)[1]
            plugin = get_symbol_parser('file%s' % ext, parser_plugins)
            if is_ignored_path(file_path, symbol_ignored_patterns):
                continue
            if not plugin:
                continue
            rel_path = os.path.relpath(file_path, root_directory)
            task_handle.report_progress(_('Indexing %r') % rel_path, -1)
            time.sleep(0.01)
            new_mtime = os.path.getmtime(file_path)
            with db.DbHelper() as dbh:
                old_mtime = dbh.get_file_mtime(file_path)
                dbh.update_file(file_path, new_mtime)
            time.sleep(0.01)
            if old_mtime is None or new_mtime > old_mtime:
                # try to parse file symbols
                parse_document(task_handle, file_id, file_path,
                               plugin, root_directory)

        # remove project paths that do not exist or that have been ignored
        task_handle.report_progress('Cleaning project index', -1)
        with db.DbHelper() as db_helper:
            for file_item in db_helper.get_files(project_ids=[proj_id]):
                path = file_item[db.COL_FILE_PATH]
                if not os.path.exists(path) or \
                        is_ignored_path(path, ignore_patterns):
                    db_helper.delete_file(path)

    task_handle.report_progress('Finished', 100)


def is_ignored_path(path, ignore_patterns=None):
    """
    Utility function that checks if a given path should be ignored.

    A path is ignored if it matches one of the ignored_patterns.

    :param path: the path to check
    :param ignore_patterns: The ignore patters to respect.
        If none, :func:hackedit.api.settings.ignore_patterns() is used instead.
    :returns: True if the path is in an directory that must be ignored
        or if the file name matches an ignore pattern, otherwise False.
    """
    if ignore_patterns is None:
        ignore_patterns = utils.get_ignored_patterns()

    def ignore(name):
        for ptrn in ignore_patterns:
            if fnmatch(name, ptrn):
                return True

    for part in os.path.normpath(path).split(os.path.sep):
        if part and ignore(part):
            return True
    return False


def scandir(task_handle, directory, ignore_patterns, root_directory):
    """
    Scan a directory recursively and returns the complete list of files.
    """
    paths = []
    rel_dir = os.path.relpath(directory, root_directory)
    task_handle.report_progress('Indexing %r' % rel_dir, -1)
    join = os.path.join
    isfile = os.path.isfile
    for path in listdir(directory):
        try:
            path = path.name
        except AttributeError:
            _logger().debug('using the old python api for scanning dirs')
        full_path = join(directory, path)
        ignored = is_ignored_path(full_path, ignore_patterns)
        if not ignored:
            if isfile(full_path):
                paths.append(full_path)
            else:
                paths += scandir(task_handle, full_path, ignore_patterns,
                                 root_directory)
    return paths


def parse_document(task_handle, file_id, path, plugin, root_directory):
    """
    Parse file symbols using the indexor plugins.
    """
    rel_path = os.path.relpath(path, root_directory)
    task_handle.report_progress('Parsing %r' % rel_path, -1)
    try:
        symbols = plugin.parse(path)
    except Exception as e:
        print(path, e)
    else:
        # flatten results and add to the db
        with db.DbHelper() as dbh:
            dbh.delete_file_symbols(file_id)
            _write_symbols_to_db(
                dbh, symbols, file_id, parent_id=None)
            dbh.conn.commit()


def _write_symbols_to_db(dbh, symbols, file_id, parent_id=None):
    """
    Writes the list of symbols to the index database.
    """
    for symbol in symbols:
        assert isinstance(symbol, Definition)
        try:
            icon_theme, icon_path = symbol.icon
        except TypeError:
            icon_theme, icon_path = '', ''
        symbol_id = dbh.create_symbol(
            symbol.name, symbol.line, symbol.column, icon_theme,
            icon_path, file_id, parent_symbol_id=parent_id, commit=False)
        _write_symbols_to_db(
            dbh, symbol.children, file_id, parent_id=symbol_id)


@functools.lru_cache()
def get_symbol_parser(path, plugins):
    """
    Gets the symbol parser for the file's mimetype.
    """
    mime = mimetypes.guess_type(path)[0]
    for plugin in plugins:
        if mime in plugin.mimetypes:
            return plugin
    return None


def _logger():
    return logging.getLogger(__name__)
