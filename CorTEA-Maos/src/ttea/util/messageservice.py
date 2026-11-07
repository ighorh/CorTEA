"""Centralized Qt message dialog service.

This module provides a MessageService class for showing translated
information, warning, critical, and question dialogs in a Qt application.
"""

from typing import Optional

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox, QWidget


class MessageService:
    """
    Centralized service for displaying user messages.

    Provides a clean, translatable, and testable interface for showing
    information, warnings, errors, and confirmation dialogs. Follows
    Qt's QMessageBox signature: text first, title optional.

    Attributes
    ----------
    parent : QWidget
        The widget used as parent for all dialogs.
    title : str
        Default window title obtained from the main window.

    Methods
    -------
    __init__(parent)
        Initialize the message service.
    info(text, title=None)
        Show an information message dialog.
    warning(text, title=None)
        Show a warning message dialog.
    critical(text, title=None)
        Show a critical error message dialog.
    question(text, title=None, default_no=True)
        Show a Yes/No question dialog with translated buttons.

    Examples
    --------
    >>> msg = MessageService(self)
    >>> msg.info("Operation completed successfully!")
    >>> if msg.question("Delete this item?", "Confirm"):
    ...     delete_item()
    """

    def __init__(self, parent: QWidget):
        """
        Initialize the message service.

        Parameters
        ----------
        parent : QWidget
            Parent widget used for dialog ownership and translation.
        """
        self.parent = parent

        # Climb to main window to get proper title
        main_window = parent
        while main_window.parent() is not None:
            main_window = main_window.parent()
        self.title = main_window.windowTitle()

    def info(self, text: str, title: Optional[str] = None) -> None:
        """
        Display an information message dialog.

        Parameters
        ----------
        text : str
            The message body to display.
        title : str, optional
            Dialog title. Uses main window title if not provided.

        Returns
        -------
        None
        """
        QMessageBox.information(self.parent, title or self.title, text)

    def warning(self, text: str, title: Optional[str] = None) -> None:
        """
        Display a warning message dialog.

        Parameters
        ----------
        text : str
            The warning message to display.
        title : str, optional
            Dialog title. Uses main window title if not provided.

        Returns
        -------
        None
        """
        QMessageBox.warning(self.parent, title or self.title, text)

    def critical(self, text: str, title: Optional[str] = None) -> None:
        """
        Display a critical error message dialog.

        Parameters
        ----------
        text : str
            The error message to display.
        title : str, optional
            Dialog title. Uses main window title if not provided.

        Returns
        -------
        None
        """
        QMessageBox.critical(self.parent, title or self.title, text)

    def question(
        self,
        text: str,
        title: Optional[str] = None,
        default_no: bool = True,
    ) -> bool:
        """
        Display a Yes/No question dialog with translated buttons.

        Parameters
        ----------
        text : str
            The question text to display.
        title : str, optional
            Dialog title. Uses main window title if not provided.
        default_no : bool, default True
            If True, "No" is the default button; otherwise "Yes".

        Returns
        -------
        bool
            True if user clicked "Yes" (Sim), False if "No" (Não).
        """
        # The "MessageService" context is explicitly specified because
        # standard QMessageBox buttons do not inherit the translation
        # context from the parent widget. This ensures that the
        # translations defined under the MessageService context
        # in the .ts file are applied.
        msg_box = QMessageBox(self.parent)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle(title or self.title)
        msg_box.setText(text)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(
            QMessageBox.No if default_no else QMessageBox.Yes
        )
        msg_box.button(QMessageBox.Yes).setText(
            QCoreApplication.translate("MessageService", "Sim")
        )
        msg_box.button(QMessageBox.No).setText(
            QCoreApplication.translate("MessageService", "Não")
        )

        return msg_box.exec() == QMessageBox.Yes

    @staticmethod
    def critical_global(text: str, title: Optional[str] = None) -> None:
        """Show a critical dialog when no parent widget is available.

        Parameters
        ----------
        text : str
            The error message to display.
        title : str, optional
            Dialog title. Uses the application title if not provided.

        Returns
        -------
        None
            Displays a modal critical message box without requiring a real
            parent widget.

        Notes
        -----
        This method creates a temporary hidden QWidget to satisfy Qt's
        parent requirement for modal dialogs.

        Examples
        --------
        >>> MessageService.critical_global('Fatal error occurred.', 'Error')
        """
        from ttea.app import AppConfig

        window = QWidget()
        window.setWindowTitle(title or AppConfig.get_title())
        window.setWindowIcon(QIcon(AppConfig.ICON_APP))
        MessageService(window).critical(text)

        window.deleteLater()
