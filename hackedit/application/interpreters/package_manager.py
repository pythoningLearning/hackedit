import logging
import os

from hackedit.application.utilities.blocking_process import BlockingProcess


class Package:
    """
    Stores the data of a package.
    """
    def __init__(self):
        self.name = ''
        self.current_version = ''
        self.latest_version = ''

    @property
    def outdated(self):
        """
        Tells whether the package is outdated or not
        """
        return self.latest_version != self.current_version

    def __repr__(self):
        if self.latest_version:
            return ' '.join([self.name, self.current_version, self.latest_version])
        return ' '.join([self.name, self.current_version])


def _logger():
    return logging.getLogger(__name__)


class PackageManager:
    """
    Base class for adding an interpreter package manager to hackedit.

    This class is responsible for running the needed commands to:
        - get the list of installed packages
        - install, update or uninstall a series of packages
    """
    def __init__(self, config):
        """
        :param config: InterpreterConfig
        """
        self.config = config
        self.last_command = ''

    def get_installed_packages(self):
        """
        Returns a list of installed packages with their current and latest version.

        :rtype: [Package]
        """
        raise NotImplementedError()

    def install_packages(self, packages):
        """
        Installs the specified packages.

        :type packages: [str]

        :returns: The package manager process' exit code and output.
        :rtype: tuple(int, str)
        """
        raise NotImplementedError()

    def uninstall_packages(self, packages):
        """
        Uninstalls the specified packages.

        :type packages: [str]

        :returns: The package manager process' exit code and output.
        :rtype: tuple(int, str)
        """
        raise NotImplementedError()

    def update_packages(self, packages):
        """
        Updates the specified packages.

        :type packages: [str]

        :returns: The package manager process' exit code and output.
        :rtype: tuple(int, str)
        """
        raise NotImplementedError()

    def _run_command(self, program, args):
        self.last_command = ' '.join([program] + args)
        _logger().debug('package manager command: %s', self.last_command)
        process = BlockingProcess(print_output=False, working_dir=os.path.expanduser('~'))
        exit_code, output = process.run(program, args)
        _logger().debug('exit code: %d', exit_code)
        _logger().debug('output:\n%s', output)
        return exit_code, output
