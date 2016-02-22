"""
Low level api for managing the file/symbols index.
"""
import logging
import os
import re
import sqlite3


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

#: name of the file id column
COL_FILE_ID = 'FILE_ID'
#: name of the file path column
COLUMN_FILE_PATH = 'FILE_PATH'
#: name of the file mtime column
COL_FILE_TIME_STAMP = 'FILE_TIME_STAMP'

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

# File CRUD
#: sql statement used to create a file in the index
SQL_CREATE_FILE = "INSERT INTO File(FILE_PATH, FILE_NAME) VALUES('%s', '%s');"
#: sql statement used to update a file in the index
SQL_UPDATE_FILE = """UPDATE File SET FILE_TIME_STAMP={0}
WHERE FILE_ID = {1};"""
#: sql statement used to remove a file from the index
SQL_DELETE_FILE = 'DELETE FROM File where FILE_ID = {0}'

# File utilities
#: sql statement used to count the number of files in the database
SQL_COUNT_FILES = """SELECT COUNT(*) FROM FILE
WHERE FILE_PATH == "%s";"""
#: sql statement to retrieve all files from the index
SQL_GET_ALL_FILES = 'SELECT * FROM File;'
#: sql statement to retrieve a filtered list of files based on fuzzy matching
#: regex
SQL_GET_FILTERED_FILES = 'SELECT * FROM File WHERE FILE_NAME REGEXP "{0}";'


def fn_regexp(expr, item):
    """
    REGEXP function that will be added to sqlite, in order to implement fuzzy
    matching (use re.findall instead of re.search to find all possible
    subsequences).
    """
    reg = re.compile(expr, re.IGNORECASE)
    matches = [m for m in reg.findall(item) if m]
    return bool(matches)


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
        self.conn.create_function("REGEXP", 2, fn_regexp)
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

    # FILE CRUD Operations
    def create_file(self, file_path):
        """
        Adds a file to the database (if the file does not already exists).

        :returns: a bool indicating whether some changes has been done (True
          if the file was added, False if the file already exists in the
          database).
        """
        if not self.has_file(file_path):
            file_name = os.path.split(file_path)[1]
            statement = SQL_CREATE_FILE % (file_path, file_name)
            c = self.conn.cursor()
            c.execute(statement)
            self.conn.commit()
            return True
        return False

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
        _logger().warn(statement)
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
        _logger().warn(statement)
        c.execute(statement)

    # Utility methods related to files management
    def has_file(self, file_path):
        """
        Checks if the file exists in the database.

        :returns: True if the file has been added to the db.
        """
        return self.file_count(file_path) > 0

    def file_count(self, file_path):
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
        statement = SQL_GET_FILTERED_FILES.format(
            get_search_regex(name_filter))
        _logger().warn('get_files statements: %r', statement)
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
        statement = 'SELECT * FROM File where FILE_PATH = "{0}"'.format(path)
        _logger().warn(statement)
        c.execute(statement)
        return c.fetchone()

    def _create_tables(self):
        """
        Creates the two index tables: one for the file index and one for the
        symbol index.
        """
        c = self.conn.cursor()
        for statement in SQL_CREATE_TABLES:
            c.execute(statement)
        self.conn.commit()


def get_search_regex(query):
    """
    Returns a regex pattern to search for query letters in order.

    :param query: String to search in another string
    :returns: regex pattern

    .. notes:
        This function adds '?.*?' between the query characters in order to
        match any subsequence of those charachters. This is an approximation
        that works well for single words fuzzy matching and is quite fast
        compared to fuzzywuzzy. To use this regex, one need to use re.findall
        or re.finditer in order to find all subsequences.

        See the regex example on pythex:
        http://pythex.org/?regex=f%3F.*%3Fi%3F.*%3Fs%3F.*%3FW%3F.*%3Fd%3F.*%3Fl%3F.*%3Fe%3F.*%3F&test_string=%27file.txt%27%2C%20%0A%27file.py%27%2C%20%0A%27other.txt%27%0A%27fiswdle%27%0A%27fistworkdle%27.&ignorecase=1&multiline=0&dotall=0&verbose=0
    """
    query = re.escape(query.replace(' ', ''))
    return ''.join(
        [(char + '?.*?') if char != '\\' else char for char in query])


def _logger():
    return logging.getLogger(__name__)
