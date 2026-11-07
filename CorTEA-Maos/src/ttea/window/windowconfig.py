"""Window configuration helpers for exergame windows.

This module provides the WindowConfig class, which centralizes common
window setup logic such as title, icon, sizing, and centering.
"""

from typing import Optional, Tuple

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget


class WindowConfig:
    """Class for fixed window configurations of the exergame application.

    This class provides methods to configure and manage window properties,
    such as title, icon, size, and positioning, with options to adjust size
    based on percentage increments or decrements relative to a parent window
    or screen.

    Attributes
    ----------
    STAY_SIZE : int
        Constant indicating that the window size should remain unchanged
        (value: 0).
    INCREMENT_SIZE_PERCENT : int
        Constant indicating that the window size should be increased by a
        percentage (value: 1).
    DECREMENT_SIZE_PERCENT : int
        Constant indicating that the window size should be decreased by a
        percentage (value: 2).

    Methods
    -------
    setup_window(title, icon, status=STAY_SIZE, width=0, height=0, parent=None)
        Configures the window properties such as title, icon, size,
        and position.
    get_base_size(parent)
        Returns the base size based on the parent window or the screen.
    adjust_size(base, percent, status)
        Adjusts the base size according to the status and percentage provided.
    center_window(parent=None, width=None, height=None)
        Centers the window relative to the parent window or the screen.
    """

    STAY_SIZE = 0
    INCREMENT_SIZE_PERCENT = 1
    DECREMENT_SIZE_PERCENT = 2

    def setup_window(
        self,
        title: Optional[str] = None,
        icon: Optional[str] = None,
        status: int = STAY_SIZE,
        width: float = 0.0,
        height: float = 0.0,
        parent: Optional[QWidget] = None,
    ) -> None:
        """Configure window properties including title, icon, size,
        and position.

        This method sets the window's title and icon, calculates the base size
        based on the parent or screen, adjusts the size according
        to the provided status and percentage, and centers the window.

        Parameters
        ----------
        title : str
            The title to be set for the window.
        icon : str
            The file path to the icon to be set for the window.
        status : int, optional
            The size adjustment status. Must be one of `STAY_SIZE`,
            `INCREMENT_SIZE_PERCENT`, or `DECREMENT_SIZE_PERCENT`.
            Default is `STAY_SIZE` (0).
        width : float, optional
            Percentage adjustment for the window width. Ignored if `status` is
            `STAY_SIZE`. Default is 0.
        height : float, optional
            Percentage adjustment for the window height. Ignored if `status` is
            `STAY_SIZE`. Default is 0.
        parent : QWidget, optional
            The parent window used for size and centering reference.
            If None, the screen geometry is used. Default is None.

        Returns
        -------
        None

        Notes
        -----
        - The window is set to a fixed size after configuration to prevent
        resizing.
        - The `width` and `height` parameters represent percentage adjustments
          (e.g., 10 means 10%) and are applied only if `status` is
          `INCREMENT_SIZE_PERCENT` or `DECREMENT_SIZE_PERCENT`.
        """
        if title is not None:
            self.setWindowTitle(title)

        if icon is not None:
            self.setWindowIcon(QIcon(icon))

        # Calculate the initial base size
        base_width, base_height = self.get_base_size(parent)

        # Adjust the size based on the status
        new_width = self.adjust_size(base_width, width, status)
        new_height = self.adjust_size(base_height, height, status)

        # Set the size and center the window
        self.center_window(parent, new_width, new_height)
        self.setFixedSize(new_width, new_height)

    def get_base_size(
        self, parent: Optional[QWidget] = None
    ) -> Tuple[int, int]:
        """Retrieve the base size based on the parent window or screen.

        If a parent window is provided, its geometry is used to determine the
        base size. Otherwise, the base size is derived from half the screen's
        width and height.

        Parameters
        ----------
        parent : QWidget, optional
            The parent window for size reference. If None, the screen geometry
            is used. Default is None.

        Returns
        -------
        tuple of int
            A tuple containing the base width and height (in pixels).

        Notes
        -----
        - If the parent is provided but lacks a `geometry` attribute,
        the screen geometry is used as a fallback.
        - The screen size is obtained from the primary screen via QApplication.
        """
        if parent is not None and hasattr(parent, "geometry"):
            parent_geo = parent.geometry()
            return parent_geo.width(), parent_geo.height()
        screen = QApplication.primaryScreen().geometry()
        return screen.width() // 2, screen.height() // 2

    def adjust_size(self, base: float, percent: float, status: int) -> float:
        """Adjust the base size based on the provided status and percentage.

        The base size is adjusted by the given percentage if the status
        indicates an increment or decrement. If the percentage is zero
        or negative, or if the status is `STAY_SIZE`,
        the base size is returned unchanged.

        Parameters
        ----------
        base : float
            The base size (width or height) to be adjusted, in pixels.
        percent : float
            The percentage adjustment to apply (e.g., 10 for 10%).
        status : int
            The adjustment status. Must be one of `STAY_SIZE`,
            `INCREMENT_SIZE_PERCENT`, or `DECREMENT_SIZE_PERCENT`.

        Returns
        -------
        float
            The adjusted size in pixels.

        Notes
        -----
        - If `percent` is less than or equal to 0, no adjustment is made,
        and the base size is returned.
        - The adjustment is calculated as a percentage of the base size.
        """

        if percent <= 0:
            return base
        if status == self.INCREMENT_SIZE_PERCENT:
            return base + (base * percent / 100)
        if status == self.DECREMENT_SIZE_PERCENT:
            return base - (base * percent / 100)
        return base

    def center_window(
        self,
        parent: Optional[QWidget] = None,
        width: Optional[float] = None,
        height: Optional[float] = None,
    ) -> None:
        """Center the window relative to the parent window or screen.

        The window is positioned at the center of the parent window if
        provided, or the screen if no parent is specified.
        The window's width and height are used unless explicitly provided.

        Parameters
        ----------
        parent : QWidget, optional
            The parent window for centering reference. If None, the screen is
            used.
            Default is None.
        width : float, optional
            The window width in pixels. If None, the current window width is
            used.
            Default is None.
        height : float, optional
            The window height in pixels. If None, the current window height is
            used.
            Default is None.

        Returns
        -------
        None

        Notes
        -----
        - The window's position is calculated to center it based on the
        provided or current width and height.
        - If the parent lacks a `geometry` attribute, the screen geometry is
        used.
        """
        if width is None:
            width = self.width()
        if height is None:
            height = self.height()

        if parent is not None and hasattr(parent, "geometry"):
            parent_geo = parent.geometry()
            x = parent_geo.x() + (parent_geo.width() - width) // 2
            y = parent_geo.y() + (parent_geo.height() - height) // 2
        else:
            screen = QApplication.primaryScreen().geometry()
            x = (screen.width() - width) // 2
            y = (screen.height() - height) // 2
        self.setGeometry(x, y, width, height)
