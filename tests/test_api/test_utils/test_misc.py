import os
import tempfile

import pytest
from hackedit.api.utils import is_ignored_path, is_outdated


def test_is_ignored_path():
    assert is_ignored_path('file.pyc') is True
    assert is_ignored_path('file.py') is False


def create_file(path, working_dir):
    if not os.path.isabs(path):
        path = os.path.join(working_dir, path)
    with open(path, 'w') as f:
        pass

@pytest.mark.parametrize('source, destination, working_dir', [
    ('file1.py', 'file2.py', tempfile.gettempdir()),
    (os.path.join(tempfile.gettempdir(), 'file11.py'), os.path.join(tempfile.gettempdir(), 'file12.py'), '')
])
def test_is_outdated_with_valid_parameters(source, destination, working_dir, qtbot):
    create_file(source, working_dir)
    qtbot.wait(100)
    create_file(destination, working_dir)

    assert not is_outdated(source, destination, working_dir=working_dir)

    create_file(destination, working_dir)
    qtbot.wait(100)
    create_file(source, working_dir)

    assert is_outdated(source, destination, working_dir=working_dir)


def test_is_outdated_with_invalid_parameters():
    with pytest.raises(ValueError):
        is_outdated(None, '', '')
