"""
High level api for manipulating project file/symbols index.

Indexing is the process of scanning a project directory recursively to build an index of all the project files and
their symbols.

To add your own index (e.g. to perform indexing on libraries), implement :class:`hackedit.api.plugins.WorkspacePlugin`
and call `perform_indexation` to perform indexation when you plugin is activated.

To add you own symbol parser (e.g. to parse the symbols of an unsupported mime types), just implement a
:class:`hackedit.api.plugins.SymbolParserPlugin`, define the mimetypes you support and implement the parse method.
"""
import os

from hackedit.app.index import db


class File:
    """
    Represents a file entry in the index database.
    """
    def __init__(self, item):
        self.name = item[db.COL_FILE_NAME]
        self.id = item[db.COL_FILE_ID]
        self.path = item[db.COL_FILE_PATH]
        self.time_stamp = item[db.COL_FILE_TIME_STAMP]


class Symbol:
    """
    Represents a symbol entry in the index database.
    """
    def __init__(self, item):
        self.name = item[db.COL_SYMBOL_NAME]
        self.id = int(item[db.COL_SYMBOL_ID])
        self.line = int(item[db.COL_SYMBOL_LINE])
        self.column = int(item[db.COL_SYMBOL_COLUMN])
        self.icon_theme = item[db.COL_SYMBOL_ICON_THEME]
        self.icon_path = item[db.COL_SYMBOL_ICON_PATH]
        self.file_id = int(item[db.COL_SYMBOL_FILE_ID])
        parent_id = item[db.COL_SYMBOL_PARENT_SYMBOL_ID]
        if not parent_id:
            self.parent_symbol_id = None
        else:
            self.parent_symbol_id = int(parent_id)


def get_project_ids(projects):
    """
    Gets the id of the specified projects.

    :param projects: list of project paths
    :return: list of id
    """
    project_ids = []
    for proj in projects:
        with db.DbHelper() as dbh:
            p = dbh.get_project(proj)
            if p:
                project_ids.append(p[db.COL_PROJECT_ID])
    return project_ids


def get_files(name_filter='', projects=None):
    """
    Generator that yields all the File entries found in the index database.

    Client can restrict the search to the specified project paths.

    An optional name filter can be used to filter files by names.

    :param name_filter: Optional file name filter.
    :param projects: List of projects to search into. If None, all files from all indexed projects will be used.
    :return: A generator that yields class:`File`.
    """
    project_ids = None
    if projects:
        project_ids = get_project_ids(projects)
    with db.DbHelper() as dbh:
        for itm in dbh.get_files(project_ids=project_ids,
                                 name_filter=name_filter):
            yield File(itm)


def get_symbols(name_filter='', projects=None, file=None):
    """
    Generator that yields all the Symbol entries found in the index database.

    Client can restrict search to the specified projects or the specified file.

    An optional name filter can be used to filter symbols by names.

    .. note:: You cannot specify both file and project filters. It's either one or the other (or none at all).

    :param name_filter: Optional symbol name filter
    :param projects: List of projects to search into. If None, all files from all indexed projects will be used.
    :param file: File to search into.

    :return: A generator that yields :class:`Symbol`.
    """
    if projects and file:
        raise ValueError('Cannot set both file and projects parameter')
    project_ids = None
    if projects:
        project_ids = get_project_ids(projects)
    file_id = None
    if file:
        with db.DbHelper() as dbh:
            file_id = dbh.get_file_by_path(file)[db.COL_FILE_ID]
    with db.DbHelper() as dbh:
        for item in dbh.get_symbols(file_id=file_id, project_ids=project_ids, name_filter=name_filter):
            file_item = dbh.get_file_by_id(item[db.COL_SYMBOL_FILE_ID])
            if item and file_item:
                yield Symbol(item), File(file_item)


def perform_indexation(directories, callback=None, task_name=None):
    """
    Perform a background indexation of the specified directory.

    The optional callback function will be called automatically when operation has finished.

    :param directory: List of directories to indexate
    :param task_name: The name of the background task as show to the users.
                      Default is "Indexing project file (project_path)".
    :param callback: Callback function (callable).
    """
    from hackedit.app.index import backend
    from ._shared import _window
    w = _window()
    ignored_patterns = w.project_explorer.get_ignored_patterns()
    parsers_plugins = w.project_explorer.parser_plugins
    args = directories, ignored_patterns, parsers_plugins
    if not task_name:
        task_name = _('Indexing project files')
    return w.task_manager.start(
        task_name, backend.index_project_files, callback, args, True, False)
