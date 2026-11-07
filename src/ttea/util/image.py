"""Load and manage images from file paths and Qt resources.

This module provides utilities for loading images from standard file
paths or Qt resource URLs, returning a pygame Surface instance.
"""

import io

import pygame
from PySide6.QtCore import QFile, QIODevice


class Image:
    """Utility class for loading and working with images.

    The class supports physical file paths and Qt resource paths (.qrc).
    """

    @staticmethod
    def load_from_qt_resource(resource_path: str) -> pygame.Surface:
        """Load an image from a Qt resource using QFile.

        Parameters
        ----------
        resource_path : str
            Qt resource path to the image file.

        Returns
        -------
        pygame.Surface
            Loaded image surface.

        Raises
        ------
        FileNotFoundError
            If the Qt resource cannot be opened.

        Examples
        --------
        >>> surface = Image.load_from_qt_resource(':/images/logo.png')
        >>> isinstance(surface, pygame.Surface)
        True
        """
        file = QFile(resource_path)
        if not file.open(QIODevice.ReadOnly):
            raise FileNotFoundError(
                f"Não foi possível abrir recurso Qt: {resource_path}."
            )

        img_data = file.readAll().data()
        file.close()
        return pygame.image.load(io.BytesIO(img_data))
