"""
Low level api for managing the file/symbols index.
"""
import logging
import os
import re
import sqlite3


# ---------------------------------------------------------
# Tables
# ---------------------------------------------------------
#: sql statements used to create the file and symbol tables.
SQL_CREATE_TABLES = [

    # File table
    """CREATE TABLE File (
        FILE_ID INTEGER PRIMARY KEY,
        FILE_PATH VARCHAR(512),
        FILE_TIME_STAMP FLOAT,
        FILE_NAME VARCHAR(256));""",

    # Symbol table
    """CREATE TABLE Symbol (
        SYMBOL_ID INTEGER PRIMARY KEY,
        SYMBOL_LINE INT,
        SYMBOL_COLUMN INT,
        SYMBOL_ICON_THEME VARCHAR(128),
        SYMBOL_ICON_PATH VARCHAR(256),
        SYMBOL_NAME VARCHAR(256),
        FILE_ID INT NOT NULL,
        PARENT_SYMBOL_ID INT,
        FOREIGN KEY(FILE_ID) REFERENCES File(FILE_ID)
        FOREIGN KEY(PARENT_SYMBOL_ID) REFERENCES Symbol(SYMBOL_ID));"""
]

# ---------------------------------------------------------
# Column names
# ---------------------------------------------------------
#: name of the file id column
COL_FILE_ID = 'FILE_ID'
#: name of the file path column
COL_FILE_PATH = 'FILE_PATH'
#: name of the file mtime column
COL_FILE_TIME_STAMP = 'FILE_TIME_STAMP'
#: name of the file mtime column
COL_FILE_NAME = 'FILE_NAME'
#: name of the symbol id column
COL_SYMBOL_ID = 'SYMBOL_ID'
#: name of the symbol line column
COL_SYMBOL_LINE = 'SYMBOL_LINE'
#: name of the symbol column column
COL_SYMBOL_COLUMN = 'SYMBOL_COLUMN'
#: name of the symbol icon theme column
COL_SYMBOL_ICON_THEME = 'SYMBOL_ICON_THEME'
#: name of the symbol icon path column
COL_SYMBOL_ICON_PATH = 'SYMBOL_ICON_PATH'
#: name of the symbol name column
COL_SYMBOL_NAME = 'SYMBOL_NAME'
#: name of the symbol file id column
COL_SYMBOL_FILE_ID = 'FILE_ID'
#: name of the symbol parent symbol id column
COL_SYMBOL_PARENT_SYMBOL_ID = 'PARENT_SYMBOL_ID'

# ---------------------------------------------------------
# SQL statements for managing files
# ---------------------------------------------------------
#: sql statement used to create a file in the index
SQL_CREATE_FILE = "INSERT INTO File(FILE_PATH, FILE_NAME) VALUES('%s', '%s');"
#: sql statement used to update a file in the index
SQL_UPDATE_FILE = """UPDATE File SET FILE_TIME_STAMP={0}
WHERE FILE_ID = {1};"""
#: sql statement used to remove a file from the index
SQL_DELETE_FILE = 'DELETE FROM File where FILE_ID = {0}'

#: sql statement used to count the number of files in the database
SQL_COUNT_FILES = """SELECT COUNT(*) FROM FILE
WHERE FILE_PATH == "%s";"""
#: sql statement to retrieve all files from the index
SQL_GET_ALL_FILES = 'SELECT * FROM File ORDER BY FILE_NAME ASC;'
#: sql statement to retrieve a filtered list of files based on fuzzy matching
#: regex
SQL_GET_FILTERED_FILES = '''SELECT * FROM File
WHERE FILE_NAME MATCH "{0}"
ORDER BY MATCH_RATIO("{0}", FILE_NAME) DESC;
'''

# ---------------------------------------------------------
# SQL statements for managing symbols
# ---------------------------------------------------------
SQL_CREATE_SYMBOL = """INSERT INTO Symbol(SYMBOL_LINE, SYMBOL_COLUMN,
SYMBOL_ICON_THEME, SYMBOL_ICON_PATH, SYMBOL_NAME, FILE_ID, PARENT_SYMBOL_ID)
values (%d, %d, "%s", "%s", "%s", %d, %s);
"""
#: sql statement used to delete all symbols attached to a specific file
SQL_DELETE_SYMBOLS = 'DELETE FROM Symbol where FILE_ID = {0}'
# Symbol utilities
#: sql statement used to retrieve all symbols of a specific file
SQL_GET_ALL_FILE_SYMBOLS = "SELECT * FROM Symbol WHERE FILE_ID = %d ORDER BY SYMBOL_NAME ASC;"
SQL_GET_FILE_SYMBOLS = '''SELECT * FROM Symbol
WHERE FILE_ID = {0} AND SYMBOL_NAME MATCH "{1}"
ORDER BY MATCH_RATIO("{1}", SYMBOL_NAME) DESC;
'''
#: sql statement to retrieve a filtered list of files based on fuzzy matching
#: regex
SQL_GET_FILTERED_SYMBOLS = '''SELECT * FROM Symbol
WHERE SYMBOL_NAME MATCH "{0}"
ORDER BY MATCH_RATIO("{0}", SYMBOL_NAME) DESC;
'''
SQL_GET_ALL_SYMBOLS = '''SELECT * FROM Symbol ORDER BY SYMBOL_NAME ASC;'''

# ---------------------------------------------------------
# Common sql statements
# ---------------------------------------------------------
#: sql statement to retrieve the last insert row id
SQL_GET_LAST_INSERT_ROW_ID = "SELECT last_insert_rowid();"


def match(expr, item):
    """
    MATCH function that will be added to sqlite, in order to implement fuzzy
    matching (use re.findall instead of re.search to find all possible
    subsequences).
    """
    return len(compute_longest_common_subsequence(expr, item)) > 0


def match_ratio(expr, item):
    """
    MATCH_RATIO function that will be added to sqlite in order to sort the
    filter list of symbols/files using fuzzy matching.

    Computes the edit distance between the given expr (user input) and an item
    from the db.
    """
    lcs = compute_longest_common_subsequence(expr, item)
    substring = lcs
    left_to_right = True
    while True:
        try:
            offset = item.index(substring)
        except ValueError:
            if left_to_right:
                substring = substring[:-1]
            else:
                substring = substring[1:]
        else:
            return len(substring) - offset / 100
        if not len(substring):
            if left_to_right:
                left_to_right = False
            else:
                return 0


class DbHelper:
    """
    Context manager that open a database connection and let you execute some
    actions on it. The connection is automatically closed when the context
    manager goes out of scope.

    .. note:: The database tables are created automatically if the database
        file did not exist.
    """
    def __init__(self, db_path):
        """
        :param db_path: Path to the database file.
        """
        self.db_path = db_path
        self.conn = None
        self.exists = os.path.exists(self.db_path)

    def __enter__(self):
        """
        Enters the context manager: creates the database if it does not exists
        and create the connection object.
        """
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.create_function("MATCH", 2, match)
        self.conn.create_function('MATCH_RATIO', 2, match_ratio)
        if not self.exists:
            _logger().debug('creating database %r', self.db_path)
            self._create_tables()
        _logger().debug('database %r created', self.db_path)
        return self

    def __exit__(self, *args, **kwargs):
        """
        Exits the context manager: closes the connection object.
        """
        self.conn.close()

    # ---------------------------------------------------------------
    # File management
    # ---------------------------------------------------------------
    # FILE CRUD Operations
    def create_file(self, file_path):
        """
        Adds a file to the database (if the file does not already exists).

        :returns: FILE_ID
        """
        if not self.has_file(file_path):
            file_name = os.path.split(file_path)[1]
            statement = SQL_CREATE_FILE % (file_path, file_name)
            c = self.conn.cursor()
            c.execute(statement)
            self.conn.commit()
            c.execute(SQL_GET_LAST_INSERT_ROW_ID)
            return c.fetchone()['last_insert_rowid()']
        else:
            f = self.get_file_by_path(file_path)
            return f[COL_FILE_ID]

    def update_file(self, file_path, mtime):
        """
        Updates a file in the database. The only data that can be update is the
        file's modification time.

        :param file_path: Path of the file to update.
        :param mtime: The new modification time of the file.

        :raises: ValueError if the file_path is not in the db.
        """
        file_row = self.get_file_by_path(file_path)
        if file_row is None:
            raise ValueError('invalid file path')
        fid = file_row[COL_FILE_ID]
        c = self.conn.cursor()
        statement = SQL_UPDATE_FILE.format(mtime, fid)
        c.execute(statement)

    def delete_file(self, file_path):
        """
        Deletes a file from the index.

        :param file_path: Path of the file to remove.
        :raises: ValueError if the file_path does not exists in the database
        """
        file_row = self.get_file_by_path(file_path)
        if file_row is None:
            raise ValueError('invalid file path')
        fid = file_row[COL_FILE_ID]
        c = self.conn.cursor()
        statement = SQL_DELETE_FILE.format(fid)
        c.execute(statement)
        self.conn.commit()
        # delete associated symbols
        self.delete_file_symbols(fid)

    # Utility methods related to files management
    def has_file(self, file_path):
        """
        Checks if the file exists in the database.

        :returns: True if the file has been added to the db.
        """
        return self.get_file_count(file_path) > 0

    def get_file_count(self, file_path):
        """
        Counts the total number of files in the database.
        """
        statement = SQL_COUNT_FILES % file_path
        c = self.conn.cursor()
        c.execute(statement)
        results = c.fetchone()
        if results:
            count = results['COUNT(*)']
        return count

    def get_files(self, name_filter):
        """
        Generates a list of filtered files.
        """
        if name_filter in [None, '']:
            raise ValueError('name_filter cannot be empty')
        statement = SQL_GET_FILTERED_FILES.format(name_filter)
        c = self.conn.cursor()
        c.execute(statement)
        while True:
            row = c.fetchone()
            if row is None:
                return
            yield row

    def get_file_mtime(self, file_path):
        """
        Gets the file's modification time from the db

        :returns: mtime - float

        :raises: ValueError if the file_path does not exists in the database
        """
        file_row = self.get_file_by_path(file_path)
        if file_row is None:
            raise ValueError('invalid file path')
        return file_row[COL_FILE_TIME_STAMP]

    def get_all_files(self):
        """
        Generates the complete list of files stored in the index.
        """
        c = self.conn.cursor()
        c.execute(SQL_GET_ALL_FILES)
        while True:
            row = c.fetchone()
            if row is None:
                return
            yield row

    def get_file_by_path(self, path):
        """
        Gets a File row from path
        """
        c = self.conn.cursor()
        statement = 'SELECT * FROM File WHERE FILE_PATH = "{0}"'.format(path)
        c.execute(statement)
        return c.fetchone()

    def get_file_by_id(self, fid):
        c = self.conn.cursor()
        statement = 'SELECT * FROM File WHERE FILE_ID = {0}'.format(fid)
        c.execute(statement)
        return c.fetchone()

    # ---------------------------------------------------------------
    # File management
    # ---------------------------------------------------------------
    # FILE CRUD Operations
    def create_symbol(self, name, line, column, icon_theme, icon_path,
                      file_id, parent_symbol_id=None):
        """
        Adds a symbol to the database.

        :param name: name of the symbol
        :param line: line where the symbol is defined
        :param column: column where the symbol is defined
        :param icon_theme: icon from theme that will be used when displaying
            the symbol
        :param icon_path: icon from path that will be used when displaying
            the symbol
        :param file_id: Id of the file where the symbol can be found
        :param parent_symbol_id: Optional parent symbol id

        returns: symbol id that can be used to add child symbols.
        """
        if parent_symbol_id is None:
            parent_symbol_id = 'null'
        statement = SQL_CREATE_SYMBOL % (
            line, column, icon_theme, icon_path, name, file_id,
            str(parent_symbol_id))
        c = self.conn.cursor()
        c.execute(statement)
        self.conn.commit()
        c.execute(SQL_GET_LAST_INSERT_ROW_ID)
        return c.fetchone()['last_insert_rowid()']

    def delete_file_symbols(self, file_id):
        """
        Removes all symbols found in the specified file_id.

        .. note:: there is no update of a symbol, symbols are always entirely
            removed from db before the update symbols are inserted
        """
        c = self.conn.cursor()
        statement = SQL_DELETE_SYMBOLS.format(file_id)
        c.execute(statement)
        self.conn.commit()

    def get_file_symbols(self, file_id, name_filter):
        """
        Generators that generates list of symbols found in the specified file
        and filtered by `name_filter`.

        :param file_id: id of the file to get the symbols from
        :param name_filter: filter symbols by name
        """
        c = self.conn.cursor()
        c.execute(SQL_GET_FILE_SYMBOLS.format(file_id, name_filter))
        while True:
            row = c.fetchone()
            if row is None:
                return
            yield row

    def get_all_file_symbols(self, file_id):
        """
        Generators that generates list of all symbols found in the specified
        file.

        :param file_id: id of the file to get the symbols from
        """
        c = self.conn.cursor()
        c.execute(SQL_GET_ALL_FILE_SYMBOLS % file_id)
        while True:
            row = c.fetchone()
            if row is None:
                return
            yield row

    def get_symbols(self, name_filter):
        """
        Generates a filtered list of symbol names (using fuzzy matching).

        :param name_filter: Filter to apply on every symbol name.
        """
        if name_filter in [None, '']:
            raise ValueError('name_filter cannot be empty')
        statement = SQL_GET_FILTERED_SYMBOLS.format(name_filter)
        c = self.conn.cursor()
        c.execute(statement)
        while True:
            row = c.fetchone()
            if row is None:
                return
            yield row

    def get_all_symbols(self):
        """
        Generates a filtered list of symbol names (using fuzzy matching).

        :param name_filter: Filter to apply on every symbol name.
        """
        c = self.conn.cursor()
        c.execute(SQL_GET_ALL_SYMBOLS)
        while True:
            row = c.fetchone()
            if row is None:
                return
            yield row

    def _create_tables(self):
        """
        Creates the two index tables: one for the file index and one for the
        symbol index.
        """
        c = self.conn.cursor()
        for statement in SQL_CREATE_TABLES:
            c.execute(statement)
        self.conn.commit()


def compute_longest_common_subsequence(a, b):
    """
    Computes longest common subsequence

    :param a: string a
    :param b: string b

    .. note:: see https://rosettacode.org/wiki/Longest_common_subsequence#Python

    :return: the longest common subsequence
    """
    lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
    # row 0 and column 0 are initialized to 0 already
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i+1][j+1] = lengths[i][j] + 1
            else:
                lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
    # read the substring out from the matrix
    result = ""
    x, y = len(a), len(b)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x-1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y-1]:
            y -= 1
        else:
            assert a[x-1] == b[y-1]
            result = a[x-1] + result
            x -= 1
            y -= 1
    return result


def _logger():
    return logging.getLogger(__name__)
