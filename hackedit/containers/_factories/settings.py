class SettingsFactory:
    def __call__(self):
        from hackedit.application.services.settings import Settings
        return Settings()
