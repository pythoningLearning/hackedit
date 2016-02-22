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


def test_create():
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
        assert dbh.create_file('/home/file.py') is True
        assert dbh.create_file('/home/file.py') is False  # already added


def test_get_files():
    remove_db()
    with db.DbHelper(DB_PATH) as dbh:
        dbh.create_file('/home/file.py')
        dbh.create_file('/home/file.txt')
        dbh.create_file('/home/zut.txt')
    with db.DbHelper(DB_PATH) as dbh:
        assert len(list(dbh.get_files('file'))) == 2
        assert len(list(dbh.get_files('files'))) == 2  # one extra letter
        assert len(list(dbh.get_files('fisWdle'))) == 2  # mispelled
        assert len(list(dbh.get_files('W'))) == 0
        assert len(list(dbh.get_files('e'))) == 2  # one letter match ok
        assert len(list(dbh.get_files('le'))) == 2
        assert len(list(dbh.get_files('zu'))) == 1
        assert len(list(dbh.get_files('zu?'))) == 1
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
        dbh.create_file(path)
        assert dbh.has_file(path)
        dbh.delete_file(path)
        assert not dbh.has_file(path)
