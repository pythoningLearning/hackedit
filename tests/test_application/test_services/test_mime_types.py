from hackedit.containers import Services
from pyqode.core.api import CodeEdit
from pyqode.core.widgets import GenericCodeEdit
from pyqode.core.widgets import TextCodeEdit


class TestMimeTypes:
    sv_mime_types = Services.mime_types()

    def test_get_supported_mimetypes(self):
        mimetypes = self.sv_mime_types.get_supported_mimetypes()
        assert len(mimetypes) >= 200
        assert 'text/x-plain' in mimetypes

    def test_get_handler_with_known_mimetype(self):
        editor = self.sv_mime_types.get_handler('text/plain')
        assert editor == TextCodeEdit

    def test_get_handler_with_unknown_mimetype(self):
        editor = self.sv_mime_types.get_handler('invalid/mimetype')
        assert editor == GenericCodeEdit

    def test_get_extensions(self):
        assert '*.txt' in self.sv_mime_types.get_extensions('text/plain')
        assert '*.texte' not in self.sv_mime_types.get_extensions('text/plain')
        assert '*.rb' in self.sv_mime_types.get_extensions('text/x-ruby')

    def test_set_extensions(self):
        self.sv_mime_types.set_extensions('text/plain', ['*.texte'])
        assert self.sv_mime_types.get_extensions('text/plain') == ['*.texte']

    def test_reset_custom_extensions(self):
        self.sv_mime_types.reset_custom_extensions()
        self.test_get_extensions()

    def test_get_mimetype_filter(self):
        assert self.sv_mime_types.get_mimetype_filter('text/x-python').startswith('text/x-python (*.py')

    def test_add_mimetype_extension_for_existing(self):
        self.sv_mime_types.reset_custom_extensions()
        self.sv_mime_types.add_mimetype_extension('text/x-python', '*.pyw')
        assert '*.pyw' in self.sv_mime_types.get_extensions('text/x-python')

    def test_add_mimetype_extension_for_new(self):
        self.sv_mime_types.reset_custom_extensions()
        self.sv_mime_types.add_mimetype_extension('text/x-spam-eggs', '*.spe')
        assert self.sv_mime_types.get_extensions('text/x-spam-eggs') == ['*.spe']

    def test_remove_mimetype_extension(self):
        self.sv_mime_types.reset_custom_extensions()
        self.test_add_mimetype_extension_for_new()
        self.sv_mime_types.remove_mimetype_extension('text/x-spam-eggs', '*.spe')
        assert self.sv_mime_types.get_extensions('text/x-spam-eggs') == []

    def test_remove_already_removed_does_not_raise(self):
        self.test_remove_mimetype_extension()
        self.sv_mime_types.remove_mimetype_extension('text/x-spam-eggs', '*.spe')
