import os

from hackedit.api import system


def test_which():
    pth = system.which('python')
    assert os.path.exists(pth)
    assert os.path.isfile(pth)
    pth = system.which('foobar')
    assert pth is None


def test_get_authenticiation_program():
    program = system.get_authentication_program()
    if system.WINDOWS:
        assert program is None
    elif system.DARWIN:
        assert program == 'pseudo'
    else:
        assert system.which(program) is not ''


def test_get_app_data_dir():
    path = system.get_app_data_directory()
    assert os.path.exists(path)


def test_get_cmd_run_command_in_terminal():
    cmd1 = system.get_cmd_run_command_in_terminal(use_hackedit_console=False)
    assert cmd1 != ''
    cmd2 = system.get_cmd_run_command_in_terminal(use_hackedit_console=True)
    assert cmd2 != ''
    assert cmd2 != cmd1


def test_get_user_workspace_dir():
    user_dir = system.get_user_workspaces_dir()
    assert system.get_app_data_directory() in user_dir
