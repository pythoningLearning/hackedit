import mimetypes


def test_python_mimetype():
    assert mimetypes.guess_type('file.py')[0] == 'text/x-python'
