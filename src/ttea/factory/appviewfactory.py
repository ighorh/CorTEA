"""Factory helpers for creating application views.

This module provides the AppViewFactory class, which centralizes the
creation of application views used across the T-TEA platform.
"""

from typing import TYPE_CHECKING, Callable, Optional

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QDialog, QMainWindow

from ttea.view import (AboutView, AutomaticCalibrationView,
                       CalibrationSettingView, CalibrationView,
                       InstitutionFacilityEditView,
                       InstitutionFacilityListView, LanguageView, MainView,
                       ManualCalibrationView, PlayerEditView,
                       PlayerGameLaunchView, PlayerListView,
                       ProfessionalEditView, ProfessionalListView)

# Type checking to prevent circular import on run time
if TYPE_CHECKING:
    from ttea.model import InstitutionFacility, Player, Professional


class AppViewFactory:
    """Factory for application view instances.

    This class provides static methods to instantiate views used in the
    application. It centralizes view construction so callers do not need
    to import view classes directly.

    Methods
    -------
    create_player_edit_view(parent=None, player=None)
        Create an instance of PlayerEditView.
    create_player_list_view(parent=None, player_edit_view=None)
        Create an instance of PlayerListView.
    create_professional_edit_view(parent=None, professional=None)
        Create an instance of ProfessionalEditView.
    create_professional_list_view(parent=None, professional_edit_view=None)
        Create an instance of ProfessionalListView.
    create_institutionfacility_edit_view(parent=None, institutionfacility=None)
        Create an instance of InstitutionFacilityEditView.
    create_institutionfacility_list_view(parent=None, institutionfacility_edit_view=None)
        Create an instance of InstitutionFacilityListView.
    create_about_view(parent=None)
        Create an instance of AboutView.
    create_calibration_view(parent=None)
        Create an instance of CalibrationView.
    create_playergamelauch_view(parent=None)
        Create an instance of PlayerGameLaunchView.
    create_language_view(parent=None)
        Create an instance of LanguageView.
    create_main_view(parent=None)
        Create an instance of MainView.
    create_manualcalibration_view(parent=None)
        Create an instance of ManualCalibrationView.
    create_automaticcalibration_view(parent=None)
        Create an instance of AutomaticCalibrationView.
    """

    @staticmethod
    def create_player_edit_view(
        parent: Optional[QDialog] = None, player: Optional["Player"] = None
    ) -> PlayerEditView:
        """
        Create an instance of PlayerEditView.

        Parameters
        ----------
        parent : Optional[QDialog], optional
            The parent dialog for the PlayerEditView, by default None.
        player : Optional[Player], optional
            The player object to be edited, by default None.

        Returns
        -------
        PlayerEditView
            An instance of PlayerEditView configured with the provided
            parent and player.
        """
        return PlayerEditView(parent, player)

    @staticmethod
    def create_player_list_view(
        parent: Optional[QObject] = None,
        player_edit_view: Optional[
            Callable[[Optional[QDialog], Optional["Player"]], PlayerEditView]
        ] = None,
    ) -> PlayerListView:
        """
        Create an instance of PlayerListView.

        Parameters
        ----------
        parent : Optional[QObject], optional
            The parent object for the PlayerListView, by default None.
        player_edit_view : Optional[Callable], optional
            A callable to create a PlayerEditView instance, by default
            None.

        Returns
        -------
        PlayerListView
            An instance of PlayerListView configured with the provided
            parent and player_edit_view callable.
        """
        return PlayerListView(parent, player_edit_view)

    @staticmethod
    def create_professional_edit_view(
        parent: Optional[QDialog] = None,
        professional: Optional["Professional"] = None,
    ) -> ProfessionalEditView:
        """
        Create an instance of ProfessionalEditView.

        Parameters
        ----------
        parent : Optional[QDialog], optional
            The parent dialog for the ProfessionalEditView,
            by default None.
        professional : Optional[Professional], optional
            The professional object to be edited, by default None.

        Returns
        -------
        ProfessionalEditView
            An instance of ProfessionalEditView configured
            with the provided parent and professional.
        """
        return ProfessionalEditView(parent, professional)

    @staticmethod
    def create_professional_list_view(
        parent: Optional[QObject] = None,
        professional_edit_view: Optional[
            Callable[
                [Optional[QDialog], Optional["Professional"]],
                ProfessionalEditView,
            ]
        ] = None,
    ) -> ProfessionalListView:
        """Create an instance of ProfessionalListView.

        Parameters
        ----------
        parent : Optional[QObject], optional
            The parent object for the list view, by default None.
        professional_edit_view : Optional[Callable], optional
            Callable that creates a ProfessionalEditView instance, by
            default None.

        Returns
        -------
        ProfessionalListView
            Configured ProfessionalListView instance.
        """
        return ProfessionalListView(parent, professional_edit_view)

    @staticmethod
    def create_institutionfacility_edit_view(
        parent: Optional[QDialog] = None,
        institutionfacility: Optional["InstitutionFacility"] = None,
    ) -> InstitutionFacilityEditView:
        """
        Create an instance of InstitutionFacilityEditView.

        Parameters
        ----------
        parent : Optional[QDialog], optional
            The parent dialog for the InstitutionFacilityEditView,
            by default None.
        institutionfacility : Optional[InstitutionFacility], optional
            The institutionfacility object to be edited, by default None.

        Returns
        -------
        InstitutionFacilityEditView
            An instance of InstitutionFacilityEditView configured
            with the provided parent and institutionfacility.
        """
        return InstitutionFacilityEditView(parent, institutionfacility)

    @staticmethod
    def create_institutionfacility_list_view(
        parent: Optional[QObject] = None,
        institutionfacility_edit_view: Optional[
            Callable[
                [Optional[QDialog], Optional["InstitutionFacility"]],
                InstitutionFacilityEditView,
            ]
        ] = None,
    ) -> InstitutionFacilityListView:
        """Create an instance of InstitutionFacilityListView.

        Parameters
        ----------
        parent : Optional[QObject], optional
            The parent object for the list view, by default None.
        institutionfacility_edit_view : Optional[Callable], optional
            Callable that creates an InstitutionFacilityEditView instance,
            by default None.

        Returns
        -------
        InstitutionFacilityListView
            Configured InstitutionFacilityListView instance.
        """
        return InstitutionFacilityListView(
            parent, institutionfacility_edit_view
        )

    @staticmethod
    def create_about_view(parent: Optional[QDialog] = None) -> AboutView:
        """
        Create an instance of AboutView.

        Parameters
        ----------
        parent : Optional[QObject], optional
            The parent object for the AboutView, by default None.

        Returns
        -------
        AboutView
            An instance of AboutView configured with the provided parent.
        """
        return AboutView(parent)

    @staticmethod
    def create_calibration_view(
        parent: Optional[QDialog] = None,
    ) -> CalibrationView:
        """
        Create an instance of CalibrationView.

        Parameters
        ----------
        parent : Optional[QObject], optional
            The parent object for the CalibrationView, by default None.

        Returns
        -------
        CalibrationView
            An instance of CalibrationView configured with the provided parent.
        """
        return CalibrationView(parent)

    @staticmethod
    def create_playergamelauch_view(
        parent: Optional[QDialog] = None,
    ) -> PlayerGameLaunchView:
        """Create an instance of PlayerGameLaunchView.

        Parameters
        ----------
        parent : Optional[QObject], optional
            The parent object for the PlayerGameLaunchView, by default None.

        Returns
        -------
        PlayerGameLaunchView
            Instance of PlayerGameLaunchView configured with the provided
            parent.
        """
        return PlayerGameLaunchView(parent)

    @staticmethod
    def create_language_view(parent: Optional[QDialog] = None) -> LanguageView:
        """
        Create an instance of LanguageView.

        Parameters
        ----------
        parent : Optional[QObject], optional
            The parent object for the LanguageView, by default None.

        Returns
        -------
        LanguageView
            An instance of LanguageView configured with the provided
            translator and parent.
        """
        return LanguageView(parent)

    @staticmethod
    def create_main_view(parent: Optional[QMainWindow] = None) -> MainView:
        """
        Create an instance of MainView.

        Parameters
        ----------
        parent : Optional[QObject], optional
            The parent object for the MainView, by default None.

        Returns
        -------
        MainView
            An instance of MainView configured with the provided
            translator and parent.
        """
        return MainView(parent)

    @staticmethod
    def create_manualcalibration_view(
        parent: Optional[QDialog] = None,
    ) -> ManualCalibrationView:
        """Create an instance of ManualCalibrationView.

        Parameters
        ----------
        parent : Optional[QDialog], optional
            The parent dialog for the manual calibration view, by
            default None.

        Returns
        -------
        ManualCalibrationView
            An instance of ManualCalibrationView configured with the
            provided parent.
        """
        return ManualCalibrationView(parent)

    @staticmethod
    def create_automaticcalibration_view(
        parent: Optional[QDialog] = None,
    ) -> AutomaticCalibrationView:
        """Create an instance of AutomaticCalibrationView.

        Parameters
        ----------
        parent : Optional[QDialog], optional
            The parent dialog for the automatic calibration view, by
            default None.

        Returns
        -------
        AutomaticCalibrationView
            An instance of AutomaticCalibrationView configured with the
            provided parent.
        """
        return AutomaticCalibrationView(parent)

    @staticmethod
    def create_calibrationsetting_view(
        parent: Optional[QDialog] = None,
    ) -> CalibrationSettingView:
        """Create an instance of CalibrationSettingView.

        Parameters
        ----------
        parent : Optional[QDialog], optional
            The parent dialog for the calibration settings view, by
            default None.

        Returns
        -------
        CalibrationSettingView
            An instance of CalibrationSettingView configured with the
            provided parent.
        """
        return CalibrationSettingView(parent)
