"""Factory accessors for application and game view factories.

This module exposes the ViewFactory class, which provides static methods
for retrieving application-specific and game-specific view factory
instances.
"""

from ttea.factory import AppViewFactory
from ttea.games.kartea.factory import KarteaViewFactory


class ViewFactory:
    """
    Factory of factories for creating view instances for app and games modules.

    This class provides static methods to obtain factory instances
    for application views and game-specific views.
    It serves as a central point for accessing
    different view factories in the application.

    Methods
    -------
    get_app_view_factory()
        Return the factory for application views.
    get_kartea_view_factory()
        Return the factory for Kartea-related views.
    """

    @staticmethod
    def get_app_view_factory() -> AppViewFactory:
        """
        Return the factory for application views.

        Returns
        -------
        AppViewFactory
            An instance of AppViewFactory for creating application-specific
            views.
        """
        return AppViewFactory()

    @staticmethod
    def get_kartea_view_factory() -> KarteaViewFactory:
        """
        Return the factory for Kartea-related views.

        Returns
        -------
        KarteaViewFactory
            An instance of KarteaViewFactory for creating views related to
            the Kartea game.
        """
        return KarteaViewFactory()
