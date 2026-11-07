from typing import TYPE_CHECKING, Callable, Optional

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QDialog

from ttea.games.kartea.view import (PlayerKarteaConfigEditView,
                                    PlayerKarteaConfigListView)

if TYPE_CHECKING:
    from ttea.games.kartea.model import PlayerKarteaConfig


class KarteaViewFactory:
    """Factory for creating Kartea-related view instances.

    This class provides static methods to instantiate views for editing
    and listing Kartea game player configurations. It ensures that views
    are properly initialized with their controllers and optional parent
    objects.

    Attributes
    ----------
    None

    Methods
    -------
    create_player_kartea_config_edit_view(parent=None, config=None)
        Create an instance of PlayerKarteaConfigEditView with its controller.
    create_player_kartea_config_list_view(parent=None,
        player_kartea_config_edit_view_factory=None) Create an
        instance of PlayerKarteaConfigListView.
    """

    @staticmethod
    def create_player_kartea_config_edit_view(
        parent: Optional[QDialog] = None,
        config: Optional["PlayerKarteaConfig"] = None,
    ) -> PlayerKarteaConfigEditView:
        return PlayerKarteaConfigEditView(parent, config)

    @staticmethod
    def create_player_kartea_config_list_view(
        parent: Optional[QObject] = None,
        player_kartea_config_edit_view: Optional[
            Callable[
                [Optional[QDialog], Optional["PlayerKarteaConfig"]],
                PlayerKarteaConfigEditView,
            ]
        ] = None,
    ) -> PlayerKarteaConfigListView:
        return PlayerKarteaConfigListView(
            parent, player_kartea_config_edit_view
        )
