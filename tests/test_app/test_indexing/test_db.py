import os
import pytest
import sqlite3
from hackedit.app.indexing import db


DB_PATH = os.path.join(os.path.expanduser('~'), '.cache', 'test.db')


def remove_db():
    try:
        os.remove(DB_PATH)
    except OSError:
        pass
    assert not os.path.exists(DB_PATH)


def test_create_tables():
    remove_db()
    with db.DbHelper(DB_PATH):
        pass
    assert os.path.exists(DB_PATH)
    assert os.path.getsize(DB_PATH) > 0


def test_create_failure():
    db_path = '/usr/test.db'
    with pytest.raises(sqlite3.OperationalError):
        with db.DbHelper(db_path):
            pass


def test_has_file():
    remove_db()
    with db.DbHelper(DB_PATH) as dbh:
        assert not dbh.has_file('/home/file.py')
        dbh.create_file('/home/file.py')
        assert dbh.has_file('/home/file.py')


def test_add_file():
    remove_db()
    with db.DbHelper(DB_PATH) as dbh:
        assert dbh.create_file('/home/file.py') == 1
        assert dbh.create_file('/home/file.py') == 1  # already added
        assert dbh.create_file('/home/file2.py') == 2
        assert dbh.create_file('/home/file3.py') == 3


def test_get_files():
    remove_db()
    with db.DbHelper(DB_PATH) as dbh:
        dbh.create_file('/home/file.py')
        dbh.create_file('/home/file.txt')
        dbh.create_file('/home/zut.txt')
        dbh.create_file('/home/setToolTip.txt')
        dbh.create_file('/home/setCallTip.txt')
        dbh.create_file('/home/setTip.txt')
    with db.DbHelper(DB_PATH) as dbh:
        assert len(list(dbh.get_files('file'))) == 5
        assert len(list(dbh.get_files('files'))) == 5  # one extra letter
        assert len(list(dbh.get_files('fisWdle'))) == 5  # mispelled
        assert len(list(dbh.get_files('W'))) == 0
        assert len(list(dbh.get_files('e'))) == 5  # one letter match ok
        assert len(list(dbh.get_files('le'))) == 5
        assert len(list(dbh.get_files('zu'))) == 1
        assert len(list(dbh.get_files('zu?'))) == 1
        items = list(dbh.get_files('setTip'))
        assert len(items) == 6
        # make sure list is correctly ordered
        assert items[0][db.COL_FILE_NAME] == 'setTip.txt'
        assert items[1][db.COL_FILE_NAME] == 'setToolTip.txt'
        assert items[2][db.COL_FILE_NAME] == 'setCallTip.txt'
        assert items[3][db.COL_FILE_NAME] == 'file.txt'
        assert items[4][db.COL_FILE_NAME] == 'file.py'
        assert items[5][db.COL_FILE_NAME] == 'zut.txt'
        with pytest.raises(ValueError):
            list(dbh.get_files(''))


def test_get_search_regex():
    assert db.get_search_regex('fi') == 'f?.*?i?.*?'
    # test special characters in the query
    assert db.get_search_regex('f.p') == 'f?.*?\\.?.*?p?.*?'


def test_get_all_files():
    remove_db()
    with db.DbHelper(DB_PATH) as dbh:
        assert len(list(dbh.get_all_files())) == 0
        dbh.create_file('/home/file.py')
        assert len(list(dbh.get_all_files())) == 1
        dbh.create_file('/home/file.txt')
        assert len(list(dbh.get_all_files())) == 2
        dbh.create_file('/home/other.txt')
        assert len(list(dbh.get_all_files())) == 3


def test_file_timestamp():
    remove_db()
    path = '/home/file.py'
    mtime = 1456088731.7597587
    with db.DbHelper(DB_PATH) as dbh:
        with pytest.raises(ValueError):
            dbh.get_file_mtime(path)
        with pytest.raises(ValueError):
            dbh.update_file(path, mtime)
        dbh.create_file(path)
        # no time stamp
        assert dbh.get_file_mtime(path) is None
        dbh.update_file(path, mtime)
        assert dbh.get_file_mtime(path) == mtime


def test_delete_files():
    remove_db()
    path = '/home/file.py'
    with db.DbHelper(DB_PATH) as dbh:
        with pytest.raises(ValueError):
            dbh.delete_file(path)
        file_id = dbh.create_file(path)
        assert dbh.has_file(path)
        dbh.create_symbol(
            'spam', 10, 45, 'code-variable', '/path/to/icon.png', file_id)
        dbh.create_symbol(
            'eggs', 22, 45, 'code-variable', '/path/to/icon.png', file_id)
        assert len(list(dbh.get_all_file_symbols(file_id))) == 2
        dbh.delete_file(path)
        assert not dbh.has_file(path)
        assert len(list(dbh.get_all_file_symbols(file_id))) == 0


def test_add_symbols():
    remove_db()
    path = '/home/file.py'
    with db.DbHelper(DB_PATH) as dbh:
        file_id = dbh.create_file(path)
        assert len(list(dbh.get_all_file_symbols(file_id))) == 0
        symbol_id = dbh.create_symbol(
            'spam', 10, 45, 'code-variable', '/path/to/icon.png', file_id)
        assert symbol_id == 1
        symbols = list(dbh.get_all_file_symbols(file_id))
        assert len(symbols) == 1
        assert symbols[0][db.COL_SYMBOL_NAME] == 'spam'
        assert symbols[0][db.COL_SYMBOL_LINE] == 10
        assert symbols[0][db.COL_SYMBOL_COLUMN] == 45
        assert symbols[0][db.COL_SYMBOL_ICON_THEME] == 'code-variable'
        assert symbols[0][db.COL_SYMBOL_ICON_PATH] == '/path/to/icon.png'
        assert symbols[0][db.COL_SYMBOL_PARENT_SYMBOL_ID] is None
        assert symbols[0][db.COL_SYMBOL_FILE_ID] == file_id
        assert symbols[0][db.COL_SYMBOL_ID] == symbol_id


def test_get_symbols():
    remove_db()
    path = '/home/file.py'
    with db.DbHelper(DB_PATH) as dbh:
        fid = dbh.create_file(path)
        dbh.create_symbol(
            'setToolTip', 10, 45, 'code-variable', '/path/to/icon.png', fid)
        dbh.create_symbol(
            'setCallTip', 10, 45, 'code-variable', '/path/to/icon.png', fid)
        dbh.create_symbol(
            'setTip', 10, 45, 'code-variable', '/path/to/icon.png', fid)
        dbh.create_symbol(
            'word', 10, 45, 'code-variable', '/path/to/icon.png', fid)
        with pytest.raises(ValueError):
            list(dbh.get_symbols(''))
        symbols = list(dbh.get_symbols('setTip'))
        assert len(symbols) == 3
        assert symbols[0][db.COL_SYMBOL_NAME] == 'setTip'
        assert symbols[1][db.COL_SYMBOL_NAME] == 'setToolTip'
        assert symbols[2][db.COL_SYMBOL_NAME] == 'setCallTip'


def test_delete_file_symbols():
    remove_db()
    path = '/home/file.py'
    with db.DbHelper(DB_PATH) as dbh:
        file_id = dbh.create_file(path)
        dbh.create_symbol(
            'spam', 10, 45, 'code-variable', '/path/to/icon.png', file_id)
        dbh.create_symbol(
            'eggs', 22, 45, 'code-variable', '/path/to/icon.png', file_id)
        assert len(list(dbh.get_all_file_symbols(file_id))) == 2
        dbh.delete_file_symbols(file_id)
        assert len(list(dbh.get_all_file_symbols(file_id))) == 0
