from hackedit.presentation.widgets import compilers

from tests.test_api.test_compilers import create_test_config


def test_compiler_config_widget(qtbot):
    widget = compilers.CompilerConfigWidget()
    qtbot.addWidget(widget)
    cfg = create_test_config()
    widget.set_config(cfg)
    assert widget.is_dirty() is False
    assert widget.get_config().to_json() == cfg.to_json()


def test_generic_compiler_config_widget(qtbot):
    """
    :type qtbot: pytestqt.qtbot.QtBot
    """
    widget = compilers.GenericCompilerCongigWidget()
    widget.show()
    qtbot.addWidget(widget)
    cfg = create_test_config()
    widget.set_config(cfg)

    assert widget.is_dirty() is False
    assert widget.get_config().to_json() == cfg.to_json()

    assert widget.ui.list_include_paths.count() == 1
    widget.ui.list_include_paths.addItem('../include')
    assert widget.ui.list_include_paths.count() == 2
    widget.ui.list_lib_paths.addItem('../libs')
    widget.ui.edit_flags.setText(widget.ui.edit_flags.text() + ' -Wall --verbose ')
    widget.ui.edit_libs.setText(widget.ui.edit_libs.text() + ' QtWidgets QtGui    ')

    assert widget.is_dirty() is True
    assert widget.get_config().to_json() != cfg.to_json()
    updated_cfg = widget.get_config()
    assert updated_cfg.include_paths == ['/usr/share/include', '../include']
    assert updated_cfg.library_paths == ['/usr/lib', '../libs']
    assert updated_cfg.flags == ['-debug', '-Wall', '--verbose']
    assert updated_cfg.libraries == ['QtCore', 'QtWidgets', 'QtGui']