class WelcomeWindowFactory:
    def __call__(self):
        from hackedit.presentation.windows.welcome import WelcomeWindow
        return WelcomeWindow()
