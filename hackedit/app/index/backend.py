"""
This module contains the backend function that perform the actual indexation.

Those functions are run in a background task.
"""
import functools
import logging
import mimetypes
import os
import time

from pyqode.core.share import Definition

from hackedit.api.utils import is_ignored_path
from hackedit.app import mime_types
from hackedit.app.index import db


# Try to use the new scandir function, introduced in python 3.5
# also available from the scandir package on pypi
try:
    # new scandir function in python 3.5
    from os import scandir as listdir
except ImportError:
    try:
        # new scandir function from scandir package on pypi
        from scandir import scandir as listdir
    except ImportError:
        # scandir function not found, use the slow listdir function
        from os import listdir


def index_project_files(task_handle, project_directories, ignore_patterns,
                        parser_plugins):
    """
    Perform a full indexation of the project files.

    :param project_directories: the directories to scan.
    :param task_handle: task handle, to report task progress.
    :param ignore_patterns: the ignore patterns to respect.
    :param parser_plugins: the list of parser plugins.
    """
    mime_types.load()
    # adjust ignore patterns to always exclude binary files from indexation
    ignore_patterns += ['*.exe', '*.dll', '*.usr', '*.so', '*.dylib', '*.psd',
                        '*.db', '.hackedit', '.eggs', '.cache', '.git', '.svn',
                        '.hackedit', 'build', 'dist', '_build']
    parser_plugins = tuple(parser_plugins)
    # create projects
    proj_ids = []

    task_handle.report_progress(_('Creating projects'), -1)
    with db.DbHelper() as dbh:
        for project_directory in project_directories:
            proj_ids.append((dbh.create_project(project_directory),
                             project_directory))

    # create file index
    for project_id, project_directory in proj_ids:
        _recursive_index_dirs(task_handle, project_directory, ignore_patterns, project_directory,
                              project_id, parser_plugins)
        clean_project_files(task_handle, project_id, ignore_patterns)

    task_handle.report_progress('Finished', 100)


def index_documents(task_handle, files, project_id, project_directory, parser_plugins):
    """
    Parse the document content if there is a suitable parser plugin and update
    the file time stamp.

    :param task_handle: Task handle, to report progress to the frontend.
    :param files: list of files to indexate.
    :param project_id: Id of the project.
    :param project_directory: Path of the project.
    :param parser_plugins: List of parser plugins.
    """
    for file_path, file_id in files:
        ext = os.path.splitext(file_path)[1]
        plugin = _get_symbol_parser('file%s' % ext, parser_plugins)
        if not plugin:
            continue
        rel_path = os.path.relpath(file_path, project_directory)
        task_handle.report_progress(_('Indexing %r') % rel_path, -1)
        time.sleep(0.01)  # allow other process to perform a query
        new_mtime, old_mtime = _update_mtime(file_path)
        time.sleep(0.01)  # allow other process to perform a query
        if old_mtime is None or new_mtime > old_mtime:
            parse_symbols(task_handle, file_id, project_id, file_path,
                          plugin, project_directory)


def clean_project_files(task_handle, project_id, ignore_patterns):
    """
    Removes project files that do not exist or that have been ignored.

    :param task_handle: Task handle, to report progress to the frontend.
    :param project_id: Id of the project to clean.
    :param ignore_patterns: The list of ignore patterns.
    """
    task_handle.report_progress('Cleaning project index', -1)
    to_delete = []
    with db.DbHelper() as db_helper:
        for file_item in db_helper.get_files(project_ids=[project_id]):
            path = file_item[db.COL_FILE_PATH]
            if not os.path.exists(path) or \
                    is_ignored_path(path, ignore_patterns):
                to_delete.append(path)
    task_handle.report_progress('Cleaning project index', -1)
    with db.DbHelper() as db_helper:
        for path in to_delete:
            db_helper.delete_file(path, commit=False)
        db_helper.conn.commit()
        time.sleep(0.001)  # allow other process to perform a query


def _recursive_index_dirs(task_handle, directory, ignore_patterns, project_dir, project_id, parser_plugins):
    """
    Performs a recursive indexation of the specified path.

    :param task_handle: task handle, to report progress updates to the frontend.
    :param directory: path to analyse.
    :param ignore_patterns: The list of ignore patterns to respect.
    :param project_dir: The root project directory.
    :param project_id: Id of the.
    :param parser_plugins: The list of parser plugins.
    """
    paths = []
    rel_dir = os.path.relpath(directory, project_dir)
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
                _recursive_index_dirs(task_handle, full_path, ignore_patterns, project_dir, project_id, parser_plugins)

    files = []
    with db.DbHelper() as dbh:
        for path in paths:
            fid = dbh.create_file(path, project_id, commit=False)
            files.append((path, fid))
        dbh.conn.commit()
    index_documents(task_handle, files, project_id, project_dir, parser_plugins)


def _update_mtime(file_path):
    """
    Update the modification time (mtime) of the specified file.

    :param file_path: Path of the file to update.
    :return: the new and the old file modification time.
    """
    new_mtime = os.path.getmtime(file_path)
    with db.DbHelper() as dbh:
        old_mtime = dbh.get_file_mtime(file_path)
        dbh.update_file(file_path, new_mtime)
    return new_mtime, old_mtime


def parse_symbols(task_handle, file_id, project_id, path, plugin, root_directory):
    """
    Parses the symbols of the specified file using the parser plugin.

    The symbols are written to the index database.

    :param task_handle: task handle, to report progress to the frontend.
    :param file_id: id of the file to parse.
    :param project_id: parent project id.
    :param path: path of the file to parse.
    :param plugin: associated parser plugin.
    :param root_directory: project directory.
    """
    rel_path = os.path.relpath(path, root_directory)
    task_handle.report_progress('Parsing %r' % rel_path, -1)
    try:
        symbols = plugin.parse(path)
    except Exception as e:
        print(path, e)
    else:
        # write results to the database
        with db.DbHelper() as dbh:
            # delete all associated symbols
            dbh.delete_file_symbols(file_id)
            # write them all and commit once all inserts have been done to
            # improve performances
            _write_symbols_to_db(
                dbh, symbols, file_id, project_id, parent_id=None)
            dbh.conn.commit()


def _write_symbols_to_db(dbh, symbols, file_id, project_id, parent_id=None):
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
            icon_path, file_id, project_id, parent_symbol_id=parent_id, commit=False)
        _write_symbols_to_db(
            dbh, symbol.children, file_id, project_id, parent_id=symbol_id)


@functools.lru_cache()
def _get_symbol_parser(path, plugins):
    """
    Gets the symbol parser for the file's mimetype.

    :param path: path of the file.
    :param plugins: the list of parser plugins.

    :returns: SymbolParserPlugin.
    """
    mime = mimetypes.guess_type(path)[0]
    for plugin in plugins:
        if mime in plugin.mimetypes:
            return plugin
    return None


def _logger():
    return logging.getLogger(__name__)
