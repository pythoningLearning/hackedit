import gettext
import inspect
import os
import sys

import pytest
from hackedit.application import i18n


def test_available_locales():
    locales = i18n.get_available_locales()
    assert isinstance(locales, set)
    assert len(locales) > 1
    assert 'fr' in locales


def test_set_locale_fr():
    i18n.set_locale('fr')
    assert i18n.get_locale() == 'fr'


def setup_gettext_mock(mocker):
    mocker.spy(gettext, 'translation')

def get_expected_locale_dir():
    return os.path.join(sys.prefix, 'share', 'locale')


@pytest.mark.parametrize('package', ['hackedit', 'hackedit-python', 'hackedit-cobol'])
def test_get_translation_for_valid_package(mocker, package):
    test_set_locale_fr()
    setup_gettext_mock(mocker)
    he_tr = i18n.get_translation(package=package)
    assert inspect.ismethod(he_tr)
    assert isinstance(he_tr.__self__, gettext.GNUTranslations)
    gettext.translation.assert_called_once_with(package, localedir=get_expected_locale_dir(),
                                                languages=[i18n.get_locale()])

def test_get_translation_for_unknown_package(mocker):
    test_set_locale_fr()
    setup_gettext_mock(mocker)
    he_tr = i18n.get_translation(package='unknown')
    assert inspect.ismethod(he_tr)
    assert isinstance(he_tr.__self__, gettext.NullTranslations)
    gettext.translation.assert_called_once_with('unknown', localedir=get_expected_locale_dir(),
                                                languages=[i18n.get_locale()])
