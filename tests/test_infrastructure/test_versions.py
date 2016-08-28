from hackedit.infrastructure import versions


def test_get_vcs_revision_does_not_fail():
    assert isinstance(versions.get_vcs_revision(), str)


def test_get_versions_dict_has_main_keys():
    component_versions = versions.get_versions()
    assert isinstance(component_versions, dict)
    assert 'hackedit' in component_versions
    assert 'python' in component_versions
    assert 'bitness' in component_versions
    assert 'qt' in component_versions
    assert 'qt_api' in component_versions
    assert 'qt_api_ver' in component_versions
    assert 'qt_api_ver' in component_versions
    assert 'system' in component_versions
    assert 'pyqode.core' in component_versions


def test_get_system_infos_is_string():
    infos = versions.get_system_infos()
    assert isinstance(infos, str)
    assert len(infos.splitlines()) >= 5
