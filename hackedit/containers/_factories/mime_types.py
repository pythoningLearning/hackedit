class MimeTypesServiceFactory:
    def __call__(self):
        from hackedit.application.services.mime_types import MimeTypesService
        return MimeTypesService()
