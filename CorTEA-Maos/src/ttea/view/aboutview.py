"""About dialog view for the T-TEA application.

This module defines the ``AboutView`` dialog, which displays project
information, developer credits, and the current year in a Qt modal window.
"""

from datetime import datetime
from typing import Optional

from PySide6.QtWidgets import QDialog

from ttea.ui import Ui_AboutView
from ttea.window import WindowConfig


class AboutView(QDialog, Ui_AboutView, WindowConfig):
    """Modal dialog showing information about the T-TEA project.

    This dialog displays the T-TEA project description, logo, platform link,
    developer credits, and a close button. It inherits from ``QDialog`` and
    uses ``WindowConfig`` for window sizing and positioning.

    Attributes
    ----------
    lbl_developer : QLabel
        Label widget that displays the developer credits and current year.

    Methods
    -------
    __init__(parent=None)
        Initialize the AboutView dialog.
    """

    def __init__(
        self,
        parent: Optional[QDialog] = None,
    ) -> None:
        """Initialize the AboutView dialog.

        Parameters
        ----------
        parent : QDialog, optional
            Parent widget for the dialog. Defaults to None.

        Notes
        -----
        Sets up the dialog UI, configures window dimensions, and updates the
        developer label with the current year.
        """

        super().__init__(parent)
        self.setupUi(self)

        self.setup_window(
            None,
            None,
            WindowConfig.DECREMENT_SIZE_PERCENT,  # status
            25,  # width
            0,  # height
            parent,  # parent
        )

        # === Dynamic part: year and translation ===
        current_year = datetime.now().strftime("%Y")

        # Translatable text
        year_text = self.tr("Desde: 2021 - {}").format(current_year)

        # HTML for the year line only
        year_html = f"""
        <p align="center" style="margin-top:12px; margin-bottom:12px;">
        <span style="font-size:10pt; font-weight:700; font-style:italic;">
            {year_text}
        </span>
        </p>
        """
        base_html = self.lbl_developer.toHtml()

        updated_html = base_html.replace("</body>", year_html + "</body>")

        self.lbl_developer.setHtml(updated_html)
