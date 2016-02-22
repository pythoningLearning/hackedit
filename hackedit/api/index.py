"""
High level api for manipulating project file/symbols index.

Indexing is the process of scanning a project directory recursively to build
an index of all the project files and their symbols.

To add your own index (e.g. to perform indexing on libraries), implement
:class:`hackedit.api.plugins.WorkspacePlugin`, create and register an
:class:`Index` instance and call `perform_indexation` to perform indexation
when you plugin is activated.

To add you own symbol parser (e.g. to parse the symbols of an unuspported
mimetype), just implement a :class:`hackedit.api.plugins.SymbolParserPlugin`
and define the mimetypes you support.
"""
from hackedit.app.indexing import db


class File:
    """
    Represents a file entry in the index database.
    """
    pass


class Symbol:
    """
    Rerpresents a symbol entry in the index database.
    """
    pass


class Index:
    """
    High level api for interacting with the index database.
    """
    def __init_(self, db_path):
        """
        Creates the database if it does not exists yet.

        :param db_path: Path to the index database
        """
        if db_path in ['', None]:
            raise ValueError("invalid db path")
        self.db_path = db_path
        # create db if it does not already exists
        db.create_database(db_path)

    def files(self, name_filter=''):
        """
        Gets the list of files for a specific project that match the optional
        name filter. If name_filter is empty, filtering is disabled. If
        project_id is None, all files are returned.
        """
        pass

    def symbols(self, name_filter='', file_id=None, top_level_only=False):
        """
        Gets the list of symbols stored in the database. You can specify a
        name file, a file filter and you have the option to only get top top
        level symbols.

        :param name_filter: name match filter
        :param file_id: if specified, only symbols that are part of the
            specified file id will be included.
        :param top_level_only: If true, only the top level symbols will be
            include (symbols that have not parent symbol). Default is False.
        """
        pass

    def add_file(self, file_path):
        """
        Adds a file.
        """
        pass

    def remove_file(self, file_path):
        """
        Removes a file.
        """
        pass

    def update_file_symbols(self, file_path, symbols):
        """
        Updates the symbols of a file.
        """
        pass


def register_index(index):
    """
    Registers an index for use by the plugins and the file/symbol locator.

    :param index: index to register.
    :type index: Index
    """
    pass


def get_all():
    """
    Gets the list of registered index.

    :returns: a list of :class:`Index`
    """
    pass


def perform_indexation(index, path, task_name, callback=None):
    """
    Performs indexation on the given path using the specified index.

    Indexation is an asynchrone operation that happens in a background process,
    you can specify a callback function to be executed once the operation has
    completed.

    :param index: index database to use for the indexing operation.
    :type: index: hackedit.api.index.Index

    :param path: path to analyze.
    :type path: str

    :param task_name: name of the task as shown in the task manager view.
    :type task_name: str

    :param callback: Optional callback function that will get called once the
        operation has completed.
    :type callback: callable
    """
    pass
