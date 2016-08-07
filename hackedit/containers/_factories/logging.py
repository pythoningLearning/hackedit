class LoggingSystemFactory:
    def __call__(self):
        from hackedit.application.services.logging import DefaultLoggingSystem
        return DefaultLoggingSystem()
