import logging

from hackedit.api import system
from hackedit.containers import Services


def test_get_application_log():
    log = Services.logging().get_application_log()
    assert isinstance(log, str)


def test_get_log_path():
    assert system.get_app_data_directory() in Services.logging().get_logs_path()


def test_get_log_files():
    log_files = Services.logging().get_log_files()
    assert isinstance(log_files, list)
    assert 1 <= len(log_files) < 7


def test_clear_log_files():
    failures = Services.logging().clear_logs()
    assert not failures
    log_files = Services.logging().get_log_files()
    assert len(log_files) == 0


def test_set_level():
    log = Services.logging()
    log.set_level(logging.INFO)
    logging.debug("debug msg 1")
    logging.info("info msg 1")

    assert 'info msg 1' in log.get_application_log()
    assert 'debug msg 1' not in log.get_application_log()

    log.set_level(logging.DEBUG)
    logging.debug("debug msg 2")
    logging.info("info msg 2")

    assert 'info msg 2' in log.get_application_log()
    assert 'debug msg 2' in log.get_application_log()