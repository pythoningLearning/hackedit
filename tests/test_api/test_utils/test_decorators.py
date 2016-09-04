import builtins

import pytest
from hackedit.application.utils import memoize_args

def test_memoize_args_working_function(mocker):
    mocker.spy(builtins, 'print')
    @memoize_args
    def test_function(argument, keyworded=''):
        print(argument, keyworded)
        return 4

    result = test_function('argument', 'keyworded')
    assert result == 4
    print.assert_called_once_with('argument', 'keyworded')
    print.reset_mock()

    result = test_function('argument', 'keyworded')
    assert result == 4
    print.assert_not_called()


def test_memoize_args_working_that_raises_exeception():
    @memoize_args
    def test_function(argument, keyworded=''):
        raise ValueError('value error: invalid arguments:%r %r' % (argument, keyworded))

    with pytest.raises(ValueError):
        test_function('arg')
