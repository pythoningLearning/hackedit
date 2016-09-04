import glob
import logging
import os

import coloredlogs
from hackedit.application import system

#: reference to the file handler
file_handler = None


FIELD_STYLES = dict(
    asctime=dict(color='green'),
    hostname=dict(color='magenta'),
    levelname=dict(color='magenta', bold=True),
    programname=dict(color='cyan'),
    name=dict(color='cyan'))

LEVEL_STYLES = dict(
    debug=dict(color='green'),
    info=dict(),
    pyqodedebug=dict(color='green'),
    pyqodedebugcomm=dict(color='green'),
    warning=dict(color='yellow'),
    error=dict(color='red'),
    critical=dict(color='red', bold=True))


class DefaultLoggingSystem:
    def __init__(self):
        super().__init__()
        self._file_handler = None
        if len(self.get_log_files()) > 5:  # pragma: no cover
            self.clear_logs()
        self._file_handler = logging.FileHandler(self.get_logs_path())
        handlers = [self._file_handler]
        fmt = '%(levelname)s %(asctime)s:%(msecs)03d %(name)s[%(process)d]  %(message)s'
        datefmt = '%H:%M:%S'
        logging.basicConfig(level=logging.INFO, handlers=handlers, format=fmt, datefmt=datefmt)
        self._logger = logging.getLogger()
        coloredlogs.install(level=logging.INFO, fmt=fmt, datefmt=datefmt, reconfigure=False,
                            field_styles=FIELD_STYLES, level_styles=LEVEL_STYLES, logger=self._logger)
        self._file_handler.setLevel(logging.INFO)

    def get_application_log(self):
        try:
            with open(self.get_logs_path(), 'r') as f:
                content = f.read()
            return content
        except OSError:
            return ''

    def clear_logs(self):
        if self._file_handler:
            self._file_handler.close()
        failures = []
        for filename in self.get_log_files():
            pth = os.path.join(system.get_app_data_directory(), filename)
            try:
                os.remove(pth)
            except OSError:
                if os.path.exists(pth):
                    logging.getLogger('hackedit').exception('failed to remove log file %r', pth)
                    failures.append(pth)
        return failures

    def set_level(self, level):
        self._logger.setLevel(level=level)
        for handler in self._logger.handlers:
            handler.setLevel(level)

    @staticmethod
    def get_logs_path():
        return os.path.join(system.get_app_data_directory(), 'hackedit-%d.log' % os.getpid())

    @staticmethod
    def get_log_files():
        return glob.glob(os.path.join(system.get_app_data_directory(), '*.log'))
