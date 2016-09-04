from hackedit.containers import View


class TestIcons:
    @classmethod
    def setup_class(cls):
        cls.icons = View.icons()

    def test_icon_themes_not_empty(self):
        assert len(self.icons.icon_themes()) > 0
