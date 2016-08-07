import builtins

import pytest
from dependency_injector import containers, providers, injections


class Eggs:
    def spam(self):
        print('spam eggs')


class HenHouse(containers.DeclarativeContainer):
    eggs = providers.Factory(Eggs)


class Spam:
    @injections.inject(eggs=HenHouse.eggs)
    def __init__(self, eggs=None):
        self.eggs = eggs

    def spam(self):
        self.eggs.spam()


def test_normal_case(mocker):
    mocker.spy(builtins, 'print')
    spam = Spam()
    spam.spam()
    print.assert_called_once_with('spam eggs')


def test_overriding(mocker):
    class MyEggs:
        def spam(self):
            print('my eggs')

    mocker.spy(builtins, 'print')
    spam = Spam(eggs=MyEggs())
    spam.spam()
    print.assert_called_once_with('my eggs')

    with pytest.raises(TypeError):
        spam = Spam(MyEggs())
