"""
This layer contains the IoC containers used by the most outer layer for building the object graph.

Since ``dependency_injector`` does not resolve dependencies automatically and need to be imported, the inner layers
are allowed to import this package.

Here are the main containers:

    - Services: contains the application servies such as the settings, the recents files/project managers,
    the logging systemn,...
    - View: contains the application views and some services related to the UI.

"""

from .factories import Factories
from .services import Services
from .view import View


__all__ = ['Factories', 'Services', 'View']
