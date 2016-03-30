import pytest

import pytest_hackedit
from hackedit.api import signals

from .test_window import PROJ_PATH


@pytest.mark.parametrize('signal', signals.SIGNALS)
def test_connect_slot(qtbot, signal):
    def slot():
        pass
    w = pytest_hackedit.main_window(qtbot, PROJ_PATH)
    signals.connect_slot(signal, slot)
    signals.disconnect_slot(signal, slot)
    pytest_hackedit.close_main_window(w)
